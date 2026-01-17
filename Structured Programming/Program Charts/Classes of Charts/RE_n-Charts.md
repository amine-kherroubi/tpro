# RE_n-Charts

**RE_n-charts** (Repeat-Exit charts) provide structured [[Chart Loop|loop]] control with explicit **exit statements** that can break out of multiple nested levels. Similar to the `REPEAT`-`EXIT` construct in BLISS, these charts use `RPT`–`END` blocks that repeatedly execute until an `EXIT` statement transfers control out of the loop. The parameter $n$ specifies the maximum nesting depth that can be exited in a single statement, allowing more flexible control flow than traditional while loops while maintaining structure.

RE_n-charts represent Kosaraju's alternative to the Böhm-Jacopini approach: instead of [[Control Flow as Data|encoding control as data]], they extend the control interface of structured constructs with [[Multi-Level Exit|multi-level exits]]. This keeps control as control—structural rather than encoded in variables.

---

## Inductive Definition

For every $n \geq 1$, the [[Class of Charts|class]] of $\text{RE}_n$-charts is the smallest class defined inductively as follows.

**Base cases.** Any [[Chart Action|action]] or exit statement $\text{EXIT}(i)$ for $0 \leq i \leq n$ is an $\text{RE}_n$-chart.

**Inductive cases.** If $G_1$ and $G_2$ are $\text{RE}_n$-charts and $p$ is a [[Chart Predicate|predicate]], then:

- $\text{SEQUENCE}(\text{RPT}, G, \text{END})$ is an $\text{RE}_n$-chart
- $\text{SEQUENCE}(G_1, G_2)$ is an $\text{RE}_n$-chart
- $\text{IF-THEN-ELSE}(p, G_1, G_2)$ is an $\text{RE}_n$-chart

---

## Semantics

`RPT` acts as the [[Chart Identity Action|identity action]] and marks the beginning of a repeat block.

`END` returns control to the matching `RPT`.

`RPT`–`END` pairs nest like parentheses, with each innermost block at level 1 and outer blocks at progressively higher levels.

`EXIT(i)` transfers control to the output line of the `END` that is $i$ levels higher:

- `EXIT(0)` is equivalent to the identity action
- If there are only $j < i$ enclosing levels, `EXIT(i)` has effective level $i - j$
- A complete chart must have all `EXIT` statements with effective level $0$

---

## Example

```
RPT                           ← level 2
  RPT                         ← level 1
    [loop body]
    if [condition_A] then EXIT(1)
    if [condition_B] then EXIT(2)
  END
  [continuation A]
  EXIT(1)
END
[continuation B]
```

---

## Relationship to Control Representation

RE_n-charts keep control as control. The `EXIT(k)` statement corresponds directly to an edge in the control-flow graph, with no intermediate variable storage.

---

## Preserving Structure While Extending Control

RE_n-charts maintain the benefits of structured programming:

- Syntax trees still fully describe control flow
- [[SESE Region|SESE]] regions are still identifiable (though more complex)
- Control flow remains **visibly constrained** by syntax

But they relax the restriction that each construct must have **exactly one** exit at the same structural level, allowing exits at different depths.

This is a controlled relaxation—unlike arbitrary GOTOs, multi-level exits still respect nesting structure.