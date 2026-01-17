# Chart Reducibility

**Reducibility** is a relation expressing that the behavior of one [[Flow Chart|flow chart]] can be represented by another under specified criteria. Reducibility provides a formal framework for comparing the expressiveness of different program structures.

---

## Forms of Reducibility

Three forms of reducibility are distinguished based on what aspects of program behavior must be preserved.

- [[Weak Chart Reducibility|Weak reducibility]] compares charts by their observable input-output behavior.
- [[Strong Chart Reducibility|Strong reducibility]] compares charts by both their input-output behavior and their internal computational paths.
- [[Chart Class Reducibility|Chart class reducibility]] compares classes of charts based on the weak reducibility of their elements.

---

## Default Convention

Unless otherwise specified, "reducibility" refers to weak reducibility. Weak reducibility is more permissive and more commonly used in theoretical analysis.

Strong reducibility matters when the execution path itself has observable effects, such as in programs with side effects or resource usage constraints.

---

## Applications

Reducibility provides a tool for proving that certain control structures are sufficient to express arbitrary computations. The Böhm-Jacopini theorem uses reducibility to show that sequence, conditional, and while-loop are computationally universal.

Reducibility also allows comparing different structured programming proposals. If every chart in class $C_1$ reduces to some chart in class $C_2$, then $C_2$ is at least as expressive as $C_1$.