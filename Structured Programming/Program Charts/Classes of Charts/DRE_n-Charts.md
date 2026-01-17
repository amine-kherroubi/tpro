# DRE_n-Charts

**DRE_n-charts** (DO-WHILE with Repeat-Exit) combine the repeat-exit mechanism of [[RE_n-Charts|RE_n-charts]] with traditional **while loops**, providing both structured iteration and multi-level exit capabilities. This hybrid approach allows programmers to use conventional `DO`-`WHILE` constructs for simple loops while retaining the flexibility of `EXIT` statements for complex control flow. The class extends RE_n-charts by adding the familiar `WHILE`-`DO` construct from [[D-Charts|D-charts]].

---

## Inductive Definition

For every $n \geq 1$, the [[Class of Charts|class]] of $\text{DRE}_n$-charts is the smallest class defined inductively as follows.

**Base cases.** Any [[Chart Action|action]] or exit statement $\text{EXIT}(i)$ for $0 \leq i \leq n$ is a is a $\text{DRE}_n$-chart.

**Inductive cases.** If $G_1$ and $G_2$ are $\text{DRE}_n$-charts and $p$ is a [[Chart Predicate|predicate]], then:

- $\text{SEQUENCE}(\text{RPT}, G, \text{END})$ is a $\text{DRE}_n$-chart.
- $\text{SEQUENCE}(G_1, G_2)$ is a $\text{DRE}_n$-chart.
- $\text{IF-THEN-ELSE}(p, G_1, G_2)$ is a $\text{DRE}_n$-chart.
- $\text{DO-WHILE}(q, G)$ where $q \in \{p, \neg p\}$, is a $\text{DRE}_n$-chart.