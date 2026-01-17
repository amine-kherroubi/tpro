# Strong Chart Reducibility

Let $G$ and $H$ be two [[Flow Chart|charts]]. $G$ is **strongly reducible** to $H$ (written $G \leq_s H$) if and only if every [[Chart Primitive|primitive]] of $H$ is a primitive of $G$, and for every [[Chart Interpretation|interpretation]] and every input, the [[Computational History|computational histories]] are identical for both charts.

Strong reducibility preserves the exact sequence of primitive executions. It is more restrictive than [[Weak Chart Reducibility|weak reducibility]]. If $G \leq_s H$ then $G \leq_w H$, but the converse does not hold.