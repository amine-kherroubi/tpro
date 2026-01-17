# D-Charts

**D-charts** correspond to Dijkstra's notion of **structured programs**. They are also referred to as `GOTO`-less programs. They are built exclusively from **sequencing**, **conditionals**, and **while loops**. They admit no arbitrary jumps and no [[Chart Loop|loops]] with multiple [[Loop Exit Point|exit points]].

D-charts represent the purest form of structured programming, where all control flow is expressed through [[SESE Region|SESE]] (Single-Entry Single-Exit) constructs. This ensures that every subprogram has exactly one entry point and one exit point, making the control flow visibly constrained by the [[Syntax Tree vs Control-Flow Graph|syntax tree]].

---

## Inductive Definition

The [[Class of Charts|class]] of D-charts is the smallest class defined inductively as follows.

**Base cases.** Any [[Chart Action|action]] is a D-chart.

**Inductive cases.** If $G_1$ and $G_2$ are D-charts and $p$ is a [[Chart Predicate|predicate]], then:

- $\text{SEQUENCE}(G_1, G_2, \ldots, G_n)$ is a D-chart
- $\text{IF-THEN-ELSE}(p, G_1, G_2)$ is a D-chart
- $\text{DO-WHILE}(q, G)$ where $q \in \{p, \neg p\}$ is a D-chart

---

## SESE Property

Every D-chart construct maintains the SESE property:

- **Sequence**: One entry (into first component), one exit (from last component)
- **If-then-else**: One entry (the test), one exit (after reconvergence)
- **While**: One entry (the condition), one exit (after termination)

This compositional discipline ensures that the syntax tree fully determines the control-flow graph structure, with no hidden control flow.

---

## Characterization Theorem

A [[Flow Chart|chart]] is [[Weak Chart Reducibility|reducible]] to a D-chart if and only if it contains no [[Loop Reachability|reachable]] loop with two or more distinct [[Loop Exit Point|exit points]].

This theorem reveals the precise boundary of D-chart expressiveness:

- Charts with only single-exit loops can be represented structurally
- Charts with multi-exit loops require either [[Control Flow as Data|auxiliary variables]] to encode control (Böhm-Jacopini) or [[Multi-Level Exit|extended exit constructs]] (Kosaraju's hierarchy).

The restriction to single-exit loops is not arbitrary—it follows necessarily from the SESE composition principle.

---

## Control Representation

D-charts keep control as control. Control flow is implicit in the syntactic structure, with no auxiliary variables encoding control decisions.