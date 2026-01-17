# Structural vs Graph Exits

It is crucial to distinguish between two notions of "exit".

---

## Graph Exits (Local Control-Flow Edges)

These are the outgoing edges from a node in the control-flow graph. For example, an `if-then-else` construct has two outgoing edges:

- One to the "then" branch
- One to the "else" branch

---

## Structural Exit (Continuation Point)

This is the syntactic point where control resumes after the construct completes. Regardless of which internal path executes, control must **reconverge** at the same structural location.

**Example**: An `if-then-else` has:

- Two graph exits (internal branches)
- One structural exit (the reconvergence point after both branches)

```
	 test
	/    \
then       else
	\    /
	 join   ← single structural exit
```
