#!/usr/bin/env python3
"""Safety tests for the engine's guarantees, run against a fake `claude` (no agents, no spend; about 2 minutes).

  python3 tests/test_safety.py

Covers: the budget cap under crashes, audit evidence binding and verdict parsing, duplicate claim ids, empty
certs/, .DS_Store, the pause hook, the blind checker's hidden paths, the stage gate, the runner lock, and time
spent without a runner. tests/fakebin/claude stands in for Claude Code and writes each task's outputs.
"""
import json, os, shutil, signal, subprocess, sys, tempfile, time

TESTS = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.dirname(TESTS)
MR = os.path.join(PLUGIN, "bin/math-research")
HERE = tempfile.mkdtemp(prefix="math-research-tests-")
open(os.path.join(HERE, "Q.md"), "w").write("# Q\nA test question.\n")
BASE = dict(os.environ, PATH=os.path.join(TESTS, "fakebin") + os.pathsep + os.environ["PATH"],
            FAKE_LOG=os.path.join(HERE, "fake.log"))
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else f"   {detail}"))


def project(name, budget=5, hours=1, **env):
    d = os.path.join(HERE, "p-" + name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    e = dict(BASE, **env)
    subprocess.run([sys.executable, MR, "new", "--name", "c", "--question", os.path.join(HERE, "Q.md"),
                    "--budget", str(budget), "--hours", str(hours)], cwd=d, env=e, check=True, capture_output=True)
    return d, e


def mr(d, e, *a):
    return subprocess.run([sys.executable, MR, *a], cwd=d, env=e, capture_output=True, text=True)


def events(d):
    return [json.loads(l) for l in open(os.path.join(d, "campaigns/c/events.jsonl")) if l.strip()]


def wait_launch(d, task, timeout=20):
    t0 = time.time()
    while time.time() - t0 < timeout:
        if os.path.exists(os.path.join(d, "campaigns/c/events.jsonl")):
            for ev in events(d):
                if ev["ev"] == "launch" and ev["task"] == task:
                    return ev
        time.sleep(0.2)


def hook(payload, env):
    p = subprocess.run([sys.executable, "-I", os.path.join(PLUGIN, "tools/pause_hook.py")],
                       input=json.dumps(payload), env=env, capture_output=True, text=True)
    return p.returncode


# 1. a killed agent is charged its whole grant
d, e = project("budget", budget=1.5, FAKE_SLEEP_research="30")
r = subprocess.Popen([sys.executable, MR, "start", "c"], cwd=d, env=e, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
ev = wait_launch(d, "research")
os.killpg(os.getpgid(ev["pid"]), signal.SIGKILL)
r.wait(timeout=60)
st = mr(d, e, "status", "c").stdout
check("1 killed agent charged its grant, workstream stops", "budget exhausted" in st or "$1.500 of $1.5" in st, st)
check("1 grant recorded at launch", ev.get("grant_usd") == 1.5, ev)
launches = [x for x in events(d) if x["ev"] == "launch"]
check("1 no relaunch after the budget is spent", len(launches) == 1, launches)

# 2 + 3 + 4. audit
def run_campaign(name, **env):
    d, e = project(name, **env)
    subprocess.run([sys.executable, MR, "start", "c"], cwd=d, env=e, capture_output=True, timeout=120)
    return d, e, mr(d, e, "audit", "c").stdout

d, e, out = run_campaign("unbound", FAKE_REVIEW_FAIL="1", FAKE_SLEEP="0.2")
check("2 review.json from a failed review is ignored", "| B | proof" in out and "**Unverified**" in out.split("| B |")[1].split("\n")[0], out)
check("2 the audit flags the unbound file", "not bound by an ACCEPTED receipt" in out, out)

d, e, out = run_campaign("errorfound", FAKE_SLEEP="0.2",
                         FAKE_REVIEW=json.dumps({"claims": {"A": "ERROR FOUND: count off by one", "B": "NO ERROR FOUND"}}))
row = lambda cid: out.split(f"| {cid} |")[1].split("\n")[0]
check("3 'ERROR FOUND: ...' refutes the claim", "Refuted or failed claim" in row("A"), out)
check("3 a proof depending on it is not lifted", "**Unverified**" in row("B"), out)

d, e, out = run_campaign("statusnames", FAKE_SLEEP="0.2",
                         FAKE_REVIEW=json.dumps({"claims": {"A": "Independently reproduced computation",
                                                            "B": "Reviewed proof; no error found"}}))
check("3 status names in the review never refute ('no error found')", "Refuted" not in out.split("## Flags")[0], out)
check("3 status names in the review never lift a claim", "**Reviewed proof" not in out and "**Independently" not in out, out)

d, e, out = run_campaign("dup", FAKE_SLEEP="0.2",
                         FAKE_CLAIMS=json.dumps([{"id": "A", "type": "finite-certificate"},
                                                 {"id": "A", "type": "proof", "statement": "main theorem"}]),
                         FAKE_CHECK=json.dumps({"claims": {"A": "PASS"}}),
                         FAKE_REVIEW=json.dumps({"claims": {"A": "CANNOT ASSESS"}}))
check("4 duplicate ids earn Unverified", "Independently reproduced" not in out.split("## Flags")[0].split("|---|")[-1], out)
check("4 duplicate ids are flagged", "used more than once" in out, out)

# 5. empty certs/ is accepted
d, e, out = run_campaign("emptycerts", FAKE_SLEEP="0.2", FAKE_EMPTY_CERTS="1")
st = mr(d, e, "status", "c").stdout
check("5 empty certs/ accepted; campaign completes", st.count(" done ") >= 5 or "BLOCKED" not in st and "review     done" in st, st)

# 10. .DS_Store in an input directory does not block
os.makedirs(os.path.join(d, "campaigns/c/ws/main/research/certs"), exist_ok=True)
open(os.path.join(d, "campaigns/c/ws/main/research/certs/.DS_Store"), "w").write("finder")
subprocess.run([sys.executable, MR, "start", "c"], cwd=d, env=e, capture_output=True, timeout=60)
st = mr(d, e, "status", "c").stdout
check("10 .DS_Store does not block the workstream", "BLOCKED" not in st, st)

# 6. pause hook
camp = os.path.join(d, "campaigns/c")
open(os.path.join(camp, "PAUSE"), "w").write("x")
he = dict(os.environ, CAMPAIGN_ROOT=camp, CAMPAIGN_WS="main", CAMPAIGN_PAUSE_FILES=os.path.join(camp, "PAUSE"))
for cmd in ("ls\npython3 step.py", "test -f PAUSE\nrm -rf ws/main/research", "ls > ws/main/research/claims.json",
            "echo x > foo", "mv certs src", "cat a.txt; rm b", "ls $(rm -rf x)"):
    check(f"6 paused: refused {cmd!r}", hook({"tool_name": "Bash", "tool_input": {"command": cmd}}, he) == 2)
for cmd in ("ls ws/main", "cat ws/main/state.json", "echo '{}' > ws/main/state.json.tmp",
            "mv ws/main/state.json.tmp ws/main/state.json"):
    check(f"6 paused: allowed {cmd!r}", hook({"tool_name": "Bash", "tool_input": {"command": cmd}}, he) == 0)
os.remove(os.path.join(camp, "PAUSE"))

# 7. hidden paths for the blind checker
spec = json.load(open(os.path.join(camp, "campaign.json")))
hidden = [t for t in spec["workstreams"]["main"]["tasks"] if t["id"] == "check"][0]["hidden"]
he = dict(he, CAMPAIGN_HIDDEN=os.pathsep.join(hidden))
refused = [("Read", {"file_path": "ws/main/research/NOTES.md"}), ("Read", {"file_path": os.path.join(camp, "ws/main/research/src/a.py")}),
           ("Read", {"file_path": "runs/research/1/out.json"}), ("Grep", {"pattern": "x"}),
           ("Glob", {"pattern": "**/*.py"}), ("Grep", {"pattern": "x", "path": "ws/main/research"}),
           ("Bash", {"command": "cat ws/main/research/NOTES.md"}), ("Bash", {"command": "cd ws/main/research && cat NOTES.md"}),
           ("Bash", {"command": "cat events.jsonl"}), ("Bash", {"command": "ls ~/.claude/projects"}),
           ("Bash", {"command": "python3 research/src/gen.py"})]
for tool, inp in refused:
    check(f"7 blind: refused {tool} {inp}", hook({"tool_name": tool, "tool_input": inp}, he) == 2)
allowed = [("Read", {"file_path": "ws/main/research/claims.json"}), ("Read", {"file_path": "QUESTION.md"}),
           ("Glob", {"pattern": "*", "path": "ws/main/research/certs"}), ("Bash", {"command": "python3 ws/main/check/chk.py"}),
           ("Bash", {"command": "ls ws/main/research/certs"}),
           ("Bash", {"command": "python3 -I tools/mark_complete.py ws/main/check/check.complete ws/main/check/CHECK.md ws/main/check/check.json"})]
for tool, inp in allowed:
    check(f"7 blind: allowed {tool} {inp}", hook({"tool_name": tool, "tool_input": inp}, he) == 0)
env_seen = [x for x in events(d) if x["ev"] == "launch"]
check("7 auto memory disabled for agents", "CLAUDE_CODE_DISABLE_AUTO_MEMORY" in open(os.path.join(PLUGIN, "tools/runner.py")).read())

# 9. gate requires a verdict for every claim
g = os.path.join(HERE, "gate")
shutil.rmtree(g, ignore_errors=True)
os.makedirs(g)
json.dump([{"id": "A"}, {"id": "B"}], open(os.path.join(g, "claims.json"), "w"))
json.dump({"claims": {"A": "PASS"}}, open(os.path.join(g, "check.json"), "w"))
subprocess.run([sys.executable, "-I", os.path.join(PLUGIN, "tools/mark_complete.py"), "gate/check.complete", "gate/check.json"],
               cwd=HERE, capture_output=True, check=True)
p = subprocess.run([sys.executable, "-I", os.path.join(PLUGIN, "tools/stage.py"), "gate", "gate/out.json", "--claims",
                    "gate/claims.json", "--allow", "PASS", "gate/check.json"], cwd=HERE, capture_output=True, text=True)
check("9 gate fails when a claim has no verdict", p.returncode == 1 and "no verdict for claims ['B']" in p.stdout, p.stdout)

# 11. two runners started together: only one runs
d, e = project("lock", FAKE_SLEEP="3")
ps = [subprocess.Popen([sys.executable, MR, "start", "c"], cwd=d, env=e, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) for _ in range(2)]
outs = [p.communicate(timeout=120)[0] for p in ps]
starts = [x for x in events(d) if x["ev"] == "runner_start"]
dup_launch = [x for x in events(d) if x["ev"] == "launch" and x["task"] == "research"]
check("11 only one runner starts", len(starts) == 1, (starts, outs))
check("11 research launched once", len(dup_launch) == 1, dup_launch)

# 8. time without a runner is charged when the runner comes back
d, e = project("gap", FAKE_SLEEP_research="12")
r = subprocess.Popen([sys.executable, MR, "start", "c"], cwd=d, env=e, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
wait_launch(d, "research")
time.sleep(1)
r.kill(); r.wait()
time.sleep(6)
st = mr(d, e, "status", "c").stdout
check("8 status warns about agents with no runner", "no runner" in st, st)
subprocess.run([sys.executable, MR, "start", "c"], cwd=d, env=e, capture_output=True, timeout=120)
gaps = [x for x in events(d) if x["ev"] == "active_time" and "without a runner" in x.get("reason", "")]
check("8 the gap is charged on adoption", gaps and gaps[0]["reason"].split("s ")[0].isdigit() and int(gaps[0]["reason"].split("s ")[0]) >= 5, gaps)

print(f"\n{sum(ok for _, ok in results)} of {len(results)} passed (work files in {HERE})")
sys.exit(0 if all(ok for _, ok in results) else 1)
