## Chart Class Reducibility

Given two [[Class of Charts|classes of charts]] $C_1$ and $C_2$, we say that $C_1$ is **reducible** to $C_2$ (written $C_1 \leq_w C_2$) if and only if for every [[Flow Chart|chart]] $G \in C_1$, there exists a chart $G' \in C_2$ such that $G \leq_w G'$, where $\leq_w$ denotes [[Weak Chart Reducibility|weak reducibility]] between charts.

---

## Properties

- If $C_1$ is reducible to $C_2$, but $C_2$ is not reducible to $C_1$, then $C_1 \lt_w C_2$, i.e. $C_1$ is **strictly reducible** to $C_2$. 
- If $C_1 \leq_w C_2$ and $C_2 \leq_w C_1$, then $C_1 \equiv_w C_2$, i.e. the two classes are **weakly equivalent**.
- If a class of charts $C_1$ is a subset of $C_2$, then $C_1 \leq_w C_2$.
- The relation $\leq_w$ is a **preorder** (transitive and reflexive).