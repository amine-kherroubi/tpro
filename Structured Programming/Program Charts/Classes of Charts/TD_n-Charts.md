# TD_n-Charts

**TD_n-charts** (Top-Down charts) model the structured decomposition philosophy of top-down programming. They enforce two principles for program reliability: 

1. Decompose each module into as few submodules as possible, especially those with multiple outputs, and
2. Minimize the number of inputs and outputs for each submodule.

The parameter $n$ limits the number of distinct [[Chart Predicate|predicates]] used without repetition, reflecting the constraint that simpler decision structures lead to more maintainable code.

---

## Inductive Definition

The [[Class of Charts|classes]] of $\text{TD}_n$-charts (Top-Down) and $\text{IP}_n$-charts (Intermediate Predicate) are defined inductively as the smallest classes satisfying the following:

**Base cases.** Any [[Chart Action|action]] is a $\text{TD}_n$-chart and any [[Chart Predicate|predicate]] is an $\text{IP}_n$-chart.

**Inductive cases.** Any $(1,j)$-chart, with $j \in \{1,2\}$, constructed from at most $n$ $\text{IP}_n$-charts (without repetitions), and any number of $\text{TD}_n$-charts is classified as:

  - A $\text{TD}_n$-chart if $j = 1$ (single output).
  - An $\text{IP}_n$-chart if $j = 2$ (two outputs).

---

## Interpretation

$IP_n$-charts represent intermediate stages in top-down development, where modules may have two outputs (like predicates), capturing hierarchical refinement. $TD_n$-charts represent complete modules with single outputs, the final result of decomposition. Limiting the number of distinct predicates to at most $n$ enforces a complexity constraint, ensuring simpler, clearer, and more maintainable programs.