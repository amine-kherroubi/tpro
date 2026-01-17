# GP_n-Charts

**GP_n-charts** (Generalized Page charts) restrict the **number of distinct predicates** used in a program, not the number of predicate occurrences. Any $(1,1)$-chart using at most $n$ distinct [[Chart Predicate|predicates]] (with repetitions allowed) can be composed into a $GP_n$-chart by substituting $GP_n$-charts for [[Chart Action|actions]]. This class models complexity constraints where the variety of decision points, rather than their frequency, determines structural complexity.

---

## Inductive Definition

For every $n \geq 1$, the [[Class of Charts|class]] of $\text{GP}_n$-charts is the smallest class defined inductively as follows.

**Base cases.** Any [[Chart Action|action]] is a $\text{GP}_n$-chart.

**General compositions.** If $G_1, G_2, \ldots, G_u$ (for $u \geq 1$) are $\text{GP}_n$-charts and $p_1, p_2, \ldots, p_i$ (for $i \leq n$) are distinct predicates, then any $(1,1)$-chart composed from $p_1, p_2, \ldots, p_i$ and $G_1, G_2, \ldots, G_u$ is a $\text{GP}_n$-chart.

Multiple occurrences of predicates are allowed, but only $i \leq n$ distinct predicates may be used.