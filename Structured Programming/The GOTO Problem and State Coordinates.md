# The GOTO Problem and State Coordinates

This document is based on *Go To Statement Considered Harmful* by Edsger W. Dijkstra.

---

## Sequential Programs

Consider a program $P$ as a sequence of statements $S_1; S_2; \ldots; S_m$. During execution, our position is characterized by a single **textual index** $i \in \{0, 1, \ldots, m\}$ meaning we've completed statements $S_1, \ldots, S_i$ and are positioned to execute $S_{i+1}$ next (with $i = m$ indicating completion).

The key property: textual adjacency in the program corresponds to temporal adjacency in execution. If we're at position $i$ and execute one step, we move to position $i+1$. This gives us a coordinate system where program structure directly reflects execution order.

---

## Conditionals and Branches

Adding conditionals like `if B then A else C` preserves the single-index property. At any moment, we're at exactly one textual position: before the conditional, inside branch $A$, inside branch $C$, or after the entire construct.

Formally, if the conditional occupies positions $i$ through $j$ in the program text, then during its execution our index $i' \in \{i, i+1, \ldots, j\}$ uniquely identifies our position. The conditional creates a control flow graph with branches, but each node still corresponds to a unique textual location. The state remains $S = (i)$.

---

## Procedures and the Call Stack

Here's where single indices become insufficient. Suppose our program contains procedures with bodies occupying disjoint regions of the program text. For concreteness, say procedure `f` occupies textual positions $[100, 150]$ and procedure `g` occupies positions $[200, 250]$.

When we call `f` from position $i = 50$, we jump to position $100$ (start of `f`'s body). The textual index alone now gives ambiguous information: being at position $120$ could mean we're executing `f` after being called from position $50$, or after being called from position $75$, or from position $300$—different call sites lead to the same textual position.

More critically, suppose `f` calls itself recursively. Then position $120$ inside `f` could represent the first invocation, the second, the third, etc. The textual index $i = 120$ doesn't distinguish these.

**Solution**: The state becomes a **call stack** $S = (i_1, i_2, \ldots, i_d)$ where:

- $d \geq 1$ is the current call depth,
- $i_d$ is the current textual position (where we are right now),
- $i_k$ for $k < d$ is the **return address** for the $k$-th stack frame (where to resume when the $(k+1)$-th call returns).

Example: If main is at position $50$, calls `f` (jumping to $100$), and `f` at position $120$ calls `g` (jumping to $200$), and we're now at position $215$ inside `g`, then $S = (51, 121, 215)$. The tuple uniquely identifies not just where we are ($215$), but the entire call chain. When `g` returns, we pop the last element and resume at $121$; when `f` returns, we resume at $51$.

The critical point: this coordinate system is **structurally generated**. We don't choose the call stack—it's determined by the program's procedure call structure. Each procedure call pushes a frame with the return address; each return pops it. The coordinates remain compositional and hierarchical.

---

## Loops and Dynamic Indices

Consider `while B do A`. A textual position inside $A$ doesn't reveal which iteration we're in. If we're at some position $i$ inside the loop body, are we in the first pass through? The tenth? This distinction matters for reasoning about correctness.

Dijkstra introduces a **dynamic index** $n \in \mathbb{N}$ for each loop: $n = 0$ before entering, $n = 1$ during the first iteration, $n = 2$ during the second, etc. This counter increments automatically with each iteration.

With nested loops, we maintain multiple dynamic indices. The state becomes $S = (i, n_1, n_2, \ldots, n_k)$ where $i$ is the textual position and $(n_1, \ldots, n_k)$ are iteration counts for currently active loops (listed inner-to-outer or by textual order—the convention doesn't matter as long as it's consistent).

Combining procedures and loops, the full state is $S = (i_1, \mathbf{n}_1, i_2, \mathbf{n}_2, \ldots, i_d, \mathbf{n}_d)$ where each stack frame $k$ has a textual position $i_k$ and a vector $\mathbf{n}_k$ of loop counters active at that depth.

These indices are **automatically generated** by program structure: entering a loop initializes its counter, each iteration increments it, exiting clears it. The programmer never manipulates these values directly.

---

## GOTO Goto Problem

An unbridled `goto` destroys this structure. If any statement can jump to any other, the same textual position $i$ becomes reachable via many different execution paths, each potentially leaving variables in different states.

What is lost is not the existence of a program counter, but the availability of a **structurally meaningful coordinate system** derived from nesting and composition. In the presence of arbitrary jumps, the coordinates induced by sequencing, procedure calls, and loop nesting no longer suffice to characterize the execution context at a point.

One can always disambiguate executions by enriching the state with full execution history—conceptually, by adding a counter $t \in \mathbb{N}$ of executed steps and considering $S = (i, t)$. The pair $(i, t)$ uniquely identifies a moment in execution.

However, $t$ is non-structural and non-compositional. To state an invariant at position $i$, one would need $\phi_v(i, t)$ accounting for all paths reaching $i$ at time $t$. This negates the abstraction benefit: invariants become path-dependent and approach the complexity of explicit execution traces.

Dijkstra's point: structured control flow (sequencing, conditionals, procedures, loops) induces coordinate systems where each position has a clear, compositional meaning. Unrestricted `goto` collapses these coordinates into an unstructured control-flow graph, forcing reasoning to become path-sensitive and undermining the locality and modularity that structured programming provides.