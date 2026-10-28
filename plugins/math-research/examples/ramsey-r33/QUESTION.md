# Question: R(3,3) = 6

## Statement
The Ramsey number R(3,3) equals 6. That is:
1. (Upper bound) In every colouring of the edges of the complete graph K6 with two colours, red and blue,
   there is a triangle whose three edges have the same colour.
2. (Lower bound) There is a two-colouring of the edges of K5 with no monochromatic triangle.

## Definitions
- K_n is the complete graph on the vertex set {0, 1, ..., n-1}; its edges are the C(n,2) pairs {i, j}, i < j.
- A two-colouring of K_n is a function c from the edges of K_n to {red, blue}.
- A monochromatic triangle is a set of three vertices {i, j, k} whose three edges {i,j}, {j,k}, {i,k} all
  receive the same colour.

## What counts as progress
Both parts established. Part 1 may be established by a written proof, by an exhaustive finite certificate, or
both. Part 2 needs an explicit colouring that anyone can check. Each part is a separate claim.

## Methods allowed
Written proofs. Exhaustive computation (there are 2^15 = 32,768 colourings of K6). No external solvers needed.

## Limits
No single computation over 2 minutes. No literature search is needed: this is a classical result.

## Background
This is a classical theorem (Greenwood and Gleason, 1955). It is used here as a small, known example to show
the research loop end to end, not as a new result.
