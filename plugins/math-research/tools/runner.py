#!/usr/bin/env python3
"""Campaign runner: durable, pausable, crash-recoverable execution of research workstreams.

The files are the authority, never a conversation:
  <campaign>/campaign.json          workstreams and tasks (frozen; its hash is checked at every start/resume)
  <campaign>/campaign.sha256        the frozen hash
  <campaign>/events.jsonl           append-only lifecycle ledger: every launch, exit, pause, resume, checkpoint,
                                    recovery, acceptance and budget event. State is rebuilt from it.
  <campaign>/ws/<W>/state.json      the workstream's research position (written by its agents)
  <campaign>/ws/<W>/HANDOVER.md     concise handover for the next agent session
  <campaign>/ws/<W>/PAUSE           present = workstream paused;  <campaign>/PAUSE = everything paused
  <campaign>/runs/<task>/<n>/       one directory per attempt: cmd, out.json, err.txt, exitcode
  <campaign>/receipts.jsonl         acceptance receipts (tools/verify.py)

Task kinds:
  agent    a headless `claude -p` session with a pre-assigned session id. Paused or interrupted sessions are
           continued with --resume <id>; if that fails, a fresh session starts from state.json + HANDOVER.md.
  compute  a command. A command that exits 75 is treated as paused and is rerun on resume; any other
           command restarts its current run only.
Completed tasks are never re-run. If a completed task's inputs change, its workstream is blocked for review.

Usage:
  runner.py --campaign DIR start [--detach]   reconcile, then run until every workstream is done, paused or blocked
  runner.py --campaign DIR pause  all|<W>     stop launching; running tasks checkpoint and stop at their next step
  runner.py --campaign DIR resume all|<W>     validate hashes and receipts, clear the pause, start the runner if needed
  runner.py --campaign DIR status
Task processes are detached from the runner, so killing the runner does not kill them; a new runner adopts them.
"""
import argparse, datetime, hashlib, json, os, signal, subprocess, sys, time, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
ACCEPT = os.path.join(HERE, "verify.py")
MANIFEST = os.path.join(HERE, "manifest_check.py")
PAUSE_HOOK = os.path.join(HERE, "pause_hook.py")
POLL = 3
PAUSED_EXIT = 75

AGENT_RULES = """You are task {task} of workstream {ws} in a durable research campaign. Working directory: {root}.
Your durable state is ws/{ws}/state.json and ws/{ws}/HANDOVER.md. They are authoritative; your own memory is not.
Rules:
1. Start by reading ws/{ws}/state.json and ws/{ws}/HANDOVER.md if they exist.
2. Work in small steps. Before each step, check whether the file ws/{ws}/PAUSE or the file PAUSE exists
   (for example with `ls`). If either exists: bring ws/{ws}/state.json and ws/{ws}/HANDOVER.md up to date,
   then reply with the single word PAUSED and stop.
3. After each completed step, update ws/{ws}/state.json (write a .tmp file, then mv it into place) and append one
   JSON line {{"task": "{task}", "step": <id>, "done": true}} to ws/{ws}/steps.jsonl.
4. Never redo a step that steps.jsonl records as done.
5. When the whole task is complete, update HANDOVER.md and reply with the single word DONE."""

RESUME_PROMPT = ("You were paused or interrupted. Re-read ws/{ws}/state.json, ws/{ws}/steps.jsonl and "
                 "ws/{ws}/HANDOVER.md (authoritative), then continue task {task} from where they say. Same rules.")


# ---------------------------------------------------------------- utilities ----------
def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def sha_file(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def boot_time():
    out = subprocess.run(["sysctl", "-n", "kern.boottime"], capture_output=True, text=True).stdout
    return out.split("sec =")[1].split(",")[0].strip() if "sec =" in out else out.strip()


def alive(pid, boot):
    if not pid or boot != BOOT:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    # a zombie child of this runner counts as dead
    try:
        r = os.waitpid(pid, os.WNOHANG)
        return r == (0, 0)
    except ChildProcessError:
        return True


def write_atomic(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


BOOT = boot_time()


class Campaign:
    def __init__(self, root):
        self.root = os.path.abspath(root)
        self.events_path = os.path.join(self.root, "events.jsonl")
        with open(os.path.join(self.root, "campaign.json")) as f:
            self.spec = json.load(f)

    def p(self, *a):
        return os.path.join(self.root, *a)

    # -------------------------------------------------------------- ledger -------------
    def log(self, ev, **kw):
        rec = {"t": now(), "ev": ev, **kw}
        with open(self.events_path, "a") as f:
            f.write(json.dumps(rec) + "\n")
            f.flush()
            os.fsync(f.fileno())
        return rec

    def events(self):
        if not os.path.exists(self.events_path):
            return []
        out = []
        for line in open(self.events_path):
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:  # torn last line after a hard kill
                pass
        return out

    def state(self):
        """Rebuild every task's state from the ledger."""
        tasks = {}
        for w, ws in self.spec["workstreams"].items():
            for t in ws["tasks"]:
                tasks[t["id"]] = {"ws": w, "spec": t, "status": "pending", "attempts": 0, "pid": None,
                                  "boot": None, "session": None, "run": None, "done_inputs": None,
                                  "failures": 0, "mode": None, "grant": 0.0}
        cost = {w: 0.0 for w in self.spec["workstreams"]}
        active = {w: 0.0 for w in self.spec["workstreams"]}
        blocked = {}
        for e in self.events():
            t = tasks.get(e.get("task"))
            if e["ev"] == "launch":
                t.update(status="running", attempts=e["attempt"], pid=e["pid"], boot=e["boot"],
                         session=e.get("session") or t["session"], run=e["run"], mode=e.get("mode"),
                         grant=e.get("grant_usd") or 0.0)
            elif e["ev"] == "exit":
                t.update(status=e["status"], pid=None)
                if e["status"] in ("failed", "rejected"):
                    if t["mode"] == "resume":
                        # the old conversation could not be continued: fall back to a fresh session from the
                        # durable files, and do not count this against the task's failure allowance
                        t["session"] = None
                    else:
                        t["failures"] += 1
                if e["status"] == "done":
                    t["done_inputs"] = e.get("inputs")
                # an agent that died without reporting its cost is charged its whole grant: the budget is a hard
                # cap, so spend that cannot be measured is assumed to have reached the limit it was given
                spent = e.get("cost_usd")
                cost[t["ws"]] += spent if spent is not None else (t["grant"] if t["spec"]["kind"] == "agent" else 0.0)
            elif e["ev"] == "interrupted":
                t.update(status="interrupted", pid=None)
                cost[t["ws"]] += t["grant"] if t["spec"]["kind"] == "agent" else 0.0
            elif e["ev"] == "active_time":
                active[e["ws"]] = e["total_s"]
            elif e["ev"] == "blocked":
                blocked[e["ws"]] = e["reason"]
            elif e["ev"] == "unblocked":
                blocked.pop(e["ws"], None)
        return tasks, cost, active, blocked

    def paused_at(self, w, when):
        """Was workstream w paused at time `when` (epoch seconds)? Replayed from the ledger, because by the time an
        exit is examined the pause files may already have been cleared by a resume."""
        state = False
        for e in self.events():
            t = datetime.datetime.fromisoformat(e["t"]).timestamp()
            if t > when + 1:  # ledger times have 1 s resolution
                break
            target = e.get("target") or e.get("ws")
            if e["ev"] in ("pause", "blocked") and target in ("all", w):
                state = True
            elif e["ev"] == "resume" and target in ("all", w):
                state = False
        return state or self.paused(w)

    def paused(self, w):
        return os.path.exists(self.p("PAUSE")) or os.path.exists(self.p("ws", w, "PAUSE"))

    def input_hashes(self, spec):
        h = {}
        for rel in spec.get("inputs", []):
            for d, dirs, fs in (os.walk(self.p(rel)) if os.path.isdir(self.p(rel)) else [(None, [], [rel])]):
                dirs[:] = [x for x in dirs if x != "__pycache__"]  # the same exclusions as verify.py
                for f in fs:
                    if d and f == ".DS_Store":
                        continue
                    path = os.path.join(d, f) if d else self.p(f)
                    h[os.path.relpath(path, self.root)] = sha_file(path) if os.path.exists(path) else "MISSING"
        return h

    # -------------------------------------------------------------- validation ---------
    def validate(self):
        """Return (campaign_problems, {workstream: problems}).
        Shared dependencies (the frozen campaign spec, the integrity checks, receipts not owned by a task) block
        the whole campaign. An invalid receipt owned by one workstream's task blocks only that workstream."""
        problems, ws_problems = [], {}
        frozen = open(self.p("campaign.sha256")).read().split()[0]
        if sha_file(self.p("campaign.json")) != frozen:
            problems.append("campaign.json differs from its frozen hash")
        for chk in self.spec.get("integrity_checks", []):
            r = subprocess.run(chk["cmd"], cwd=self.root, capture_output=True, text=True)
            if r.returncode != 0:
                problems.append(f"integrity check '{chk['name']}' failed: {(r.stdout + r.stderr)[-300:]}")
        if os.path.exists(self.p("receipts.jsonl")):
            owner = {t["id"]: w for w, ws in self.spec["workstreams"].items() for t in ws["tasks"]}
            r = subprocess.run([sys.executable, "-I", ACCEPT, "verify"], cwd=self.root, capture_output=True, text=True)
            for line in r.stdout.splitlines():
                if line.startswith("INVALID: "):
                    name = line.split()[1]
                    if name in owner:
                        ws_problems.setdefault(owner[name], []).append("receipt INVALID: " + line[9:][:300])
                    else:
                        problems.append("shared receipt INVALID: " + line[9:][:300])
        return problems, ws_problems

    def block_invalid(self, ws_problems, blocked):
        for w, probs in ws_problems.items():
            if w not in blocked:
                # also pause the workstream, so a task already running stops at its next step
                os.makedirs(self.p("ws", w), exist_ok=True)
                write_atomic(self.p("ws", w, "PAUSE"), now() + "\n")
                self.log("blocked", ws=w, reason="; ".join(probs)[:600])

    # -------------------------------------------------------------- tasks --------------
    def launch(self, tid, t, resume):
        spec, w = t["spec"], t["ws"]
        ws = self.spec["workstreams"][w]
        attempt = t["attempts"] + 1
        run = os.path.join("runs", tid, str(attempt))
        os.makedirs(self.p(run), exist_ok=True)
        session = t["session"]
        mode = "fresh"
        if spec["kind"] == "agent":
            remaining = max(0.05, ws["budget_usd"] - self.state()[1][w])
            # resume_policy "session": continue the original conversation, falling back to a fresh session if it
            # fails. "fresh": always start a new session from the durable files (state.json, HANDOVER.md).
            use_session = resume and session and ws.get("resume_policy", "session") == "session"
            if use_session:
                prompt, flags, mode = RESUME_PROMPT.format(ws=w, task=tid), ["--resume", session], "resume"
            else:
                session = str(uuid.uuid4())
                prompt = open(self.p(spec["prompt"])).read()
                if t["attempts"]:
                    prompt = (f"An earlier session worked on task {tid} and is not available to you. Its progress is "
                              f"in ws/{w}/state.json, ws/{w}/steps.jsonl and ws/{w}/HANDOVER.md. Read them first, "
                              f"never redo a recorded step, and continue.\n\n" + prompt)
                flags = ["--session-id", session]
            rules = AGENT_RULES.format(task=tid, ws=w, root=self.root)
            # the pause is enforced by a PreToolUse hook, not left to the agent's compliance
            hooks = {"hooks": {"PreToolUse": [{"matcher": ".*", "hooks": [
                {"type": "command", "command": f"'{sys.executable}' -I '{PAUSE_HOOK}'"}]}]}}
            flags += ["--settings", json.dumps(hooks)]
            cmd = (["claude", "-p", prompt] + flags +
                   ["--model", spec.get("model", ws["model"]), "--permission-mode", "auto", "--output-format", "json",
                    "--max-budget-usd", f"{remaining:.2f}", "--append-system-prompt", rules])
        else:
            cmd = spec["cmd"]
        write_atomic(self.p(run, "cmd.json"), json.dumps(cmd, indent=1))
        # auto memory is off for every agent: durable state lives in the campaign's files, and a memory shared by
        # all sessions in this directory would carry the author's reasoning to the blind checker
        env = dict(os.environ, CAMPAIGN_ROOT=self.root, CAMPAIGN_WS=w, CLAUDE_CODE_DISABLE_AUTO_MEMORY="1",
                   CAMPAIGN_PAUSE_FILES=self.p("PAUSE") + os.pathsep + self.p("ws", w, "PAUSE"),
                   CAMPAIGN_HIDDEN=os.pathsep.join(spec.get("hidden", [])))
        quoted = " ".join("'" + c.replace("'", "'\\''") + "'" for c in cmd)
        sh = f"{quoted} > {run}/out.json 2> {run}/err.txt; echo $? > {run}/exitcode.tmp; mv {run}/exitcode.tmp {run}/exitcode"
        proc = subprocess.Popen(["/bin/sh", "-c", sh], cwd=self.root, env=env, start_new_session=True,
                                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.log("launch", ws=w, task=tid, attempt=attempt, pid=proc.pid, boot=BOOT, run=run, mode=mode,
                 session=session if spec["kind"] == "agent" else None,
                 grant_usd=round(remaining, 2) if spec["kind"] == "agent" else None)

    def finish(self, tid, t):
        """Classify a task whose process has gone."""
        spec, run = t["spec"], t["run"]
        ec_path = self.p(run, "exitcode")
        if not os.path.exists(ec_path):
            self.log("interrupted", ws=t["ws"], task=tid, attempt=t["attempts"], reason="process gone, no exit code")
            return
        code = int(open(ec_path).read().strip() or -1)
        cost, result = None, ""
        if spec["kind"] == "agent":
            try:
                data = json.load(open(self.p(run, "out.json")))
                res = [x for x in data if x.get("type") == "result"][-1] if isinstance(data, list) else data
                cost, result = res.get("total_cost_usd"), (res.get("result") or "").strip()
                if res.get("is_error"):
                    code = code or 1
            except (ValueError, IndexError, OSError):
                code = code or 1
            # classify from durable evidence, not from the agent's last word: a clean exit with every declared
            # output present is a completion (acceptance still checks the outputs); a clean exit while a pause
            # flag is set is a pause
            outputs_present = bool(spec.get("outputs")) and all(os.path.exists(self.p(o)) for o in spec["outputs"])
            if code == 0 and (outputs_present or (not spec.get("outputs") and result.endswith("DONE"))):
                status = "completed"
            elif code == 0 and (self.paused_at(t["ws"], os.path.getmtime(ec_path)) or result.endswith("PAUSED")):
                status = "paused"
            else:
                status = "failed"
        else:
            status = "completed" if code == 0 else "paused" if code == PAUSED_EXIT else "failed"
        if status == "completed":
            missing = [o for o in spec.get("outputs", []) if not os.path.exists(self.p(o))]
            if missing:
                status = "failed"
                result += f" [missing outputs {missing}]"
        bound = None
        if status == "completed":
            # a completion marker (an output ending in .complete, written by tools/mark_complete.py) must list every
            # other declared output with a hash that still matches the file; otherwise the task is not done
            markers = [o for o in spec.get("outputs", []) if o.endswith(".complete")]
            for m in markers:
                try:
                    bound = json.load(open(self.p(m)))["outputs"]
                except (ValueError, KeyError, OSError):
                    bound = {}
                required = [o for o in spec["outputs"] if o not in markers]
                stale = [o for o in required if o not in bound or not os.path.exists(self.p(o)) or
                         sha_file(self.p(o)) != bound[o]]
                if stale:
                    status = "failed"
                    result += f" [completion marker {m} missing or stale for {stale}]"
        inputs = None
        if status == "completed":
            # every task gets a receipt: its own checker, or the default manifest check of its declared outputs
            acc = spec.get("accept") or {"inputs": ["campaign.json"], "checker": [MANIFEST],
                                         "cmd": [sys.executable, "-I", MANIFEST, *spec.get("outputs", [])]}
            if acc:
                r = subprocess.run([sys.executable, "-I", ACCEPT, "run", tid, "--inputs", *acc["inputs"],
                                    "--checker", *acc["checker"], "--outputs", *spec.get("outputs", []),
                                    "--", *acc["cmd"]], cwd=self.root, capture_output=True, text=True)
                self.log("acceptance", ws=t["ws"], task=tid, result=r.stdout.strip()[-300:], exit=r.returncode)
                status = "done" if r.returncode == 0 else "rejected"
                if status == "done" and bound:
                    # the receipt must bind exactly the hashes the completion marker recorded
                    rec = [json.loads(l) for l in open(self.p("receipts.jsonl")) if l.strip()]
                    rec = [x for x in rec if x["name"] == tid and x["status"] == "ACCEPTED"][-1]
                    if any(rec["outputs"].get(o) != h for o, h in bound.items()):
                        status = "rejected"
                        self.log("acceptance", ws=t["ws"], task=tid, result="receipt hashes differ from marker", exit=1)
            else:
                status = "done"
            inputs = self.input_hashes(spec)
        self.log("exit", ws=t["ws"], task=tid, attempt=t["attempts"], code=code, status=status, cost_usd=cost,
                 result=result[-300:], inputs=inputs)

    # -------------------------------------------------------------- main loop ----------
    def acquire_lock(self, lock):
        """Create the lock atomically (O_EXCL), so two runners started together cannot both run. A lock whose
        runner is dead is removed and the creation retried once."""
        for _ in range(2):
            try:
                fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                try:
                    pid, boot = json.load(open(lock)).values()
                except (ValueError, OSError):  # being written by another runner right now, unless it is old
                    if time.time() - os.path.getmtime(lock) < 10:
                        print("runner already starting")
                        return False
                    pid = boot = None
                if alive(pid, boot):
                    print(f"runner already running (pid {pid})")
                    return False
                os.remove(lock)
                continue
            with os.fdopen(fd, "w") as f:
                f.write(json.dumps({"pid": os.getpid(), "boot": BOOT}))
                f.flush()
                os.fsync(f.fileno())
            return True
        print("could not acquire runner.lock")
        return False

    def run(self):
        lock = self.p("runner.lock")
        if not self.acquire_lock(lock):
            return 1
        problems, ws_problems = self.validate()
        if problems:
            self.log("runner_refused", problems=problems)
            print("refusing to run:\n  " + "\n  ".join(problems))
            os.remove(lock)
            return 2
        self.log("runner_start", pid=os.getpid(), boot=BOOT)
        tasks, _, active, blocked = self.state()
        self.block_invalid(ws_problems, blocked)
        adopted = [tid for tid, t in tasks.items() if t["status"] == "running" and alive(t["pid"], t["boot"])]
        if adopted:
            # these tasks kept running while no runner counted their time; charge the whole gap (wall clock, so it
            # may include sleep: an overcount is the safe direction for a cap)
            last = max(datetime.datetime.fromisoformat(e["t"]).timestamp() for e in self.events()
                       if e["ev"] != "runner_start")
            gap = max(0.0, time.time() - last)
            for w in {tasks[x]["ws"] for x in adopted}:
                active[w] += gap
                self.log("active_time", ws=w, total_s=round(active[w], 1), reason=f"{gap:.0f}s without a runner")
            self.log("adopted", tasks=adopted)
        checkpoints = {}
        last_tick, mono = time.time(), time.monotonic()
        while True:
            tasks, cost, _, blocked = self.state()
            # active time is accumulated in memory from the ledger value at start, using a monotonic clock,
            # which on macOS does not advance while the machine sleeps
            dt, mono = time.monotonic() - mono, time.monotonic()
            busy_ws = set()
            for tid, t in tasks.items():
                if t["status"] == "running":
                    if alive(t["pid"], t["boot"]):
                        busy_ws.add(t["ws"])
                    else:
                        self.finish(tid, t)
            for w in busy_ws:
                active[w] += dt
                # enforce the wall-clock cap on a running task: pause the workstream, so the agent checkpoints and
                # stops (the pause hook enforces this); the block below then stops further launches
                cap = self.spec["workstreams"][w]["wall_s"]
                if active[w] >= cap and not self.paused(w):
                    write_atomic(self.p("ws", w, "PAUSE"), now() + "\n")
                    self.log("pause", target=w, reason=f"wall-clock budget reached ({active[w]:.0f}s of {cap}s)")
                    self.log("active_time", ws=w, total_s=round(active[w], 1))
            if time.time() - last_tick > 30:
                for w in busy_ws:
                    self.log("active_time", ws=w, total_s=round(active[w], 1))
                last_tick = time.time()
                problems, ws_problems = self.validate()
                if problems and not os.path.exists(self.p("PAUSE")):
                    write_atomic(self.p("PAUSE"), now() + "\n")
                    self.log("pause", target="all", reason="shared dependency invalid: " + "; ".join(problems)[:500])
                self.block_invalid(ws_problems, blocked)
            # checkpoints written by agents
            for w in self.spec["workstreams"]:
                sp = self.p("ws", w, "state.json")
                if os.path.exists(sp):
                    h = sha_file(sp)
                    if checkpoints.get(w) not in (None, h):
                        self.log("checkpoint", ws=w, sha256=h)
                    checkpoints[w] = h
            tasks, cost, _, blocked = self.state()
            open_ws = 0
            for w, ws in self.spec["workstreams"].items():
                seq = [tid for tid in tasks if tasks[tid]["ws"] == w]
                if w in blocked or any(tasks[x]["status"] == "running" for x in seq):
                    open_ws += any(tasks[x]["status"] == "running" for x in seq)
                    continue
                # stale completed work blocks the workstream rather than being silently redone
                for x in seq:
                    t = tasks[x]
                    if t["status"] == "done" and t["done_inputs"] and self.input_hashes(t["spec"]) != t["done_inputs"]:
                        self.log("blocked", ws=w, reason=f"inputs of completed task {x} changed")
                        break
                else:
                    nxt = next((x for x in seq if tasks[x]["status"] != "done"), None)
                    if nxt is None:
                        continue
                    t = tasks[nxt]
                    # pauses, interruptions and unavailable sessions do not count; only genuine failures do
                    if t["status"] in ("failed", "rejected") and t["failures"] >= ws.get("max_failures", 3):
                        self.log("blocked", ws=w, reason=f"task {nxt} {t['status']}: {t['failures']} failures "
                                                         f"in {t['attempts']} attempts")
                        continue
                    if self.paused(w):
                        continue
                    if cost[w] >= ws["budget_usd"]:
                        self.log("blocked", ws=w, reason=f"budget exhausted (${cost[w]:.2f} of ${ws['budget_usd']})")
                        continue
                    if active[w] >= ws["wall_s"]:
                        self.log("blocked", ws=w, reason=f"wall-clock budget exhausted ({active[w]:.0f}s)")
                        continue
                    self.launch(nxt, t, resume=t["status"] in ("paused", "interrupted"))
                    open_ws += 1
            if open_ws == 0:
                tasks, _, _, blocked = self.state()
                if not any(t["status"] == "running" for t in tasks.values()):
                    for w in self.spec["workstreams"]:
                        self.log("active_time", ws=w, total_s=round(active[w], 1))
                    self.log("runner_idle", summary={w: self.ws_summary(w, tasks) for w in self.spec["workstreams"]})
                    os.remove(lock)
                    return 0
            time.sleep(POLL)

    def ws_summary(self, w, tasks):
        return {x: tasks[x]["status"] for x in tasks if tasks[x]["ws"] == w}


# ---------------------------------------------------------------- commands ------------
def cmd_start(c, detach):
    if detach:
        log = open(c.p("runner.log"), "a")
        p = subprocess.Popen([sys.executable, "-I", os.path.abspath(__file__), "--campaign", c.root, "start"],
                             start_new_session=True, stdin=subprocess.DEVNULL, stdout=log, stderr=log)
        print(f"runner started in background (pid {p.pid}); log: {c.p('runner.log')}")
        return 0
    return c.run()


def targets(c, which):
    return list(c.spec["workstreams"]) if which == "all" else [which]


def cmd_pause(c, which):
    path = c.p("PAUSE") if which == "all" else c.p("ws", which, "PAUSE")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    write_atomic(path, now() + "\n")
    c.log("pause", target=which)
    print(f"paused {which}: no new tasks start; running tasks checkpoint and stop at their next step")
    return 0


def cmd_resume(c, which):
    problems, ws_problems = c.validate()
    if problems:
        c.log("resume_refused", target=which, problems=problems)
        print("resume refused (shared dependency):\n  " + "\n  ".join(problems))
        return 2
    _, _, _, blocked = c.state()
    c.block_invalid(ws_problems, blocked)
    for w, probs in ws_problems.items():
        print(f"{w} stays blocked: " + "; ".join(probs)[:300])
    for path in ([c.p("PAUSE")] if which == "all" else []) + [c.p("ws", w, "PAUSE") for w in targets(c, which)]:
        if os.path.exists(path):
            os.remove(path)
    c.log("resume", target=which)
    if which != "all" and which in ws_problems:
        print(f"resume of {which} refused: its receipts are invalid")
        return 2
    lock = c.p("runner.lock")
    if os.path.exists(lock):
        pid, boot = json.load(open(lock)).values()
        if alive(pid, boot):
            print(f"resumed {which}; runner already running (pid {pid})")
            return 0
    print(f"resumed {which}")
    return cmd_start(c, detach=True)


def cmd_unblock(c, w):
    """After a human has reviewed and fixed a blocked workstream: re-check it, then clear the block."""
    problems, ws_problems = c.validate()
    if problems or w in ws_problems:
        print("still invalid:\n  " + "\n  ".join(problems + ws_problems.get(w, [])))
        return 2
    c.log("unblocked", ws=w)
    print(f"unblocked {w}")
    return 0


def cmd_status(c):
    tasks, cost, active, blocked = c.state()
    lock = c.p("runner.lock")
    runner = "not running"
    if os.path.exists(lock):
        pid, boot = json.load(open(lock)).values()
        runner = f"running (pid {pid})" if alive(pid, boot) else "not running (stale lock)"
    print(f"campaign {c.spec.get('name')}  runner {runner}  {'ALL PAUSED' if os.path.exists(c.p('PAUSE')) else ''}")
    if not runner.startswith("running") and any(t["status"] == "running" and alive(t["pid"], t["boot"])
                                                 for t in tasks.values()):
        print("  WARNING: agents are running with no runner, so the time cap is not enforced. Run start or resume.")
    for w, ws in c.spec["workstreams"].items():
        flag = "BLOCKED: " + blocked[w] if w in blocked else "paused" if c.paused(w) else "active"
        print(f"  {w}: {flag}; ${cost[w]:.3f} of ${ws['budget_usd']}; {active[w]:.0f}s of {ws['wall_s']}s")
        for x, t in tasks.items():
            if t["ws"] == w:
                live = " (process alive)" if t["status"] == "running" and alive(t["pid"], t["boot"]) else ""
                print(f"     {x:<10} {t['status']:<12} attempts {t['attempts']}{live}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--campaign", required=True)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start")
    s.add_argument("--detach", action="store_true")
    for name in ("pause", "resume", "unblock"):
        sub.add_parser(name).add_argument("which")
    sub.add_parser("status")
    a = ap.parse_args()
    c = Campaign(a.campaign)
    if a.cmd == "start":
        return cmd_start(c, a.detach)
    if a.cmd == "unblock":
        return cmd_unblock(c, a.which)
    if a.cmd == "pause":
        return cmd_pause(c, a.which)
    if a.cmd == "resume":
        return cmd_resume(c, a.which)
    return cmd_status(c)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda *a: sys.exit(143))
    sys.exit(main())
