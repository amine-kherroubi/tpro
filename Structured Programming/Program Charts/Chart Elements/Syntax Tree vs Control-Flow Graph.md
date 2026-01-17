# Syntax Tree vs Control-Flow Graph

Every program admits two representations: a **syntax tree** representing hierarchical structure, and a **control-flow graph** (CFG) representing execution paths.

---

## Syntax Trees

A **syntax tree** represents the hierarchical composition of program constructs. Programs are built by nesting constructs according to grammatical rules.

---

## Control-Flow Graphs

A **control-flow graph** represents possible execution paths as nodes and edges. Each node is a basic block, each edge is a potential control transfer.

---

## The Asymmetry

### Flowcharts

- The **graph is primary**: nodes and edges are specified directly
- No compositional constraints
- All graphs are possible

### Structured Programs

- The **syntax tree is primary**: programs are composed from nested constructs
- The graph is **derived** from syntax
- Only certain graphs are possible

---

## The Restriction

Structured syntax generates only graphs satisfying compositional constraints. Each construct has a fixed control interface:

- Sequencing has one exit (out of the last component)
- Selection has one exit (after reconvergence)
- Iteration has one exit (after loop terminates)

This compositional discipline ensures all generated subgraphs are [[SESE Region|SESE regions]].

---

## Non-Realizable Graphs

A loop with two exits to different continuations:

```
    loop_test
        ↓
    loop_body
       / \
   exit_A  exit_B
```

cannot arise from structured syntax without additional mechanisms, because structured loops have exactly one structural exit.

---

## Resolution Strategies

To represent non-realizable graphs:

1. **[[Control Flow as Data|Control as data]]**: Encode graph structure in variables (Böhm-Jacopini)
2. **[[Multi-Level Exit|Extended control]]**: Allow richer control interfaces (Kosaraju)