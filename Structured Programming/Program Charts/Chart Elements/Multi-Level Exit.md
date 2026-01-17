# Multi-Level Exit

A **multi-level exit** is a control construct that transfers control outward across $k$ nested constructs in a single statement. Unlike [[Control Flow as Data|control as data]], multi-level exits remain pure control flow—they extend the control interface of structured constructs without introducing auxiliary state.

Multi-level exits are control constructs, not data operations. An `EXIT(k)` corresponds directly to an edge in the control-flow graph, requiring no intermediate variable storage or testing.

---

## Definition

A multi-level exit construct `EXIT(k)` transfers control to the continuation point that is $k$ structural levels outward from the current position.

- `EXIT(0)`: Equivalent to the [[Chart Identity Action|identity action]]
- `EXIT(1)`: Exit the immediately enclosing loop or block
- `EXIT(k)`: Exit $k$ enclosing levels simultaneously

---

## Semantics

Given nested `RPT-END` blocks:

```
RPT                  ← level 3
  RPT                ← level 2
    RPT              ← level 1
      EXIT(k)
    END
  END
END
```

An `EXIT(k)` statement transfers control to the output line of the `END` that is $k$ levels higher in the nesting structure.

---

## Effective Level

If there are only $j < k$ enclosing levels, then `EXIT(k)` has **effective level** $k - j$ with respect to the current chart. A complete chart must have all `EXIT` statements with effective level $0$ (all exits resolve within the chart).