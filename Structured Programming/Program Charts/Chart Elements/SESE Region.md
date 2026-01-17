# SESE Region (Single-Entry Single-Exit)

A **SESE region** (Single-Entry Single-Exit) is a fundamental concept in structured programming that characterizes well-behaved control-flow subgraphs. A region in a [[Flow Chart|chart]] is SESE if it has exactly one [[Chart Entry Point|entry point]] and exactly one [[Chart Exit Point|exit point]].

---

## Formal Definition

A SESE region in a [[Flow Chart|chart]] is a subgraph with the following properties:

1. **Single Entry**: Control enters the region through exactly one syntactic point.
2. **Single Exit**: Control leaves the region through exactly one syntactic point, meaning all internal control paths reconverge to the same continuation.

---

## Graph-Theoretic Characterization

In graph theory, a SESE region is defined by an ordered edge pair $(a, b)$ where:

- $a$ dominates all nodes in the region: Every [[Chart Path|path]] from the chart's entry to any node in the region passes through edge $a$.
- $b$ postdominates all nodes in the region: Every path from any node in the region to the chart's exit passes through edge $b$.
- **Cycle property**: Every cycle containing $a$ also contains $b$ and vice versa.

---

## Why SESE Matters

SESE regions are the foundation of structured programming because:

1. **Composability**: SESE constructs can be nested arbitrarily without creating control-flow ambiguity.
2. **Syntax Constraint**: Structured syntax (sequencing, `if-then-else`, `while`) generates only SESE regions. Not every control-flow graph corresponds to a SESE region.
3. **Control as Syntax**: In SESE regions, control flow remains implicit in the syntactic structure rather than being encoded as data.

---

## Non-SESE Examples

### Loop with Two Exits
A [[Chart Loop|loop]] whose body can jump to two different continuation points outside the loop violates SESE:

```
        loop
       /    \
   exit A   exit B   ← no reconvergence
```

This cannot be represented by a simple `while` construct without either:
- Introducing auxiliary variables (program counter/flags), or
- Using multi-level exit constructs (labeled breaks).

### If-Else Without Reconvergence
If each branch of an `if-else` jumps to a different external continuation point rather than reconverging, it is **not** an `if-else` in the structured sense:

```
        test
       /    \
   then → A  else → B   ← two distinct continuations
```

This violates the single structural exit property.

---

## Connection to Structured Constructs

All standard structured programming constructs are SESE:

- **Sequence**: `S₁; S₂` has one entry (into S₁) and one exit (out of S₂)
- **Selection**: `if C then S₁ else S₂` has one entry (the test) and one exit (after reconvergence)
- **Iteration**: `while C do S` has one entry (the condition) and one exit (after the loop finishes)

---

## Relationship to Reducibility

A [[Flow Chart|chart]] can be reduced to structured form without auxiliary variables if and only if it can be decomposed into nested SESE regions. Charts with non-SESE subgraphs require either:
- **Control as data**: Program counters or flags ([[BJ_n-Charts|Böhm-Jacopini construction]])
- **Extended control**: Multi-level exits ([[RE_n-Charts|Kosaraju's hierarchy]])

---

## See Also

- [[D-Charts|D-charts]]: Structured programs built exclusively from SESE constructs
- [[Control Flow as Data|Control Flow as Data]]: How Böhm-Jacopini encode non-SESE control
- [[Multi-Level Exit|Multi-Level Exit]]: Kosaraju's alternative to encoding control as data
- [[Chart Class Reducibility|Chart Class Reducibility]]: Formal comparison of expressiveness

---
