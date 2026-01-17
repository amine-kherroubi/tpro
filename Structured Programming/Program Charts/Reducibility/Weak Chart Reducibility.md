# Weak Chart Reducibility

Let $G$ and $H$ be two [[Flow Chart|charts]]. $G$ is **weakly reducible** to $H$ (written $G \leq_w H$) if and only if:

1. Every [[Chart Primitive|primitive]] of $H$ is a primitive of $G$, and
2. For every [[Chart Interpretation|interpretation]] and every input, the outputs are equal (or both do not terminate) for both the charts.

Weak reducibility preserves input-output behavior but not necessarily the [[Computational History|computational path]].