# GRE_n-Charts

**GRE_n-charts** (Generalized Repeat-Exit charts) extend [[RE_n-Charts|RE_n-charts]] by allowing **exit statements** to jump to any $i \ge 0$ levels above the current `RPT` block, not just the $n$ immediately enclosing levels. Like [[RE_n-Charts|RE_n-charts]], they use `RPT`–`END` blocks with nested repeat structures, but each block is constrained to have at most $n$ distinct **effective levels**.

---

## Inductive Definition

For every $n \ge 1$, the [[Class of Charts|class]] of $\text{GRE}_n$-charts is defined as follows.

**Base cases.** Any [[Chart Action|action]] or $\text{EXIT}(i)$ for $i \ge 0$ is a $\text{GRE}_n$-chart, provided the effective levels in any sub-chart do not exceed $n$ distinct nonzero values.

**Inductive cases.** If $G_1$ and $G_2$ are $\text{GRE}_n$-charts and $p$ is a [[Chart Predicate|predicate]], then:

- $\text{SEQUENCE}(\text{RPT}, G, \text{END})$ is a $\text{GRE}_n$-chart.
- $\text{SEQUENCE}(G_1, G_2)$ is a $\text{GRE}_n$-chart.
- $\text{IF-THEN-ELSE}(p, G_1, G_2)$ is a $\text{GRE}_n$-chart.

The **effective levels** of a sub-chart are the nonzero levels of all its `EXIT` statements together with 0; no sub `RPT`–`END` block may have more than $n$ distinct effective levels.