# BJ_n-Charts

**BJ_n-charts** extend [[D-Charts|D-charts]] with generalized [[Chart Loop|loop]] constructs that allow up to $n$ exit conditions. They are named after Böhm and Jacopini, who proposed these structures to overcome limitations of `GOTO`-less programming while maintaining structured syntax.

BJ_n-charts achieve universal expressiveness by implicitly using [[Control Flow as Data|control as data]]—the $\Omega$ construct encodes multiple exit conditions that, in implementation, require a program counter or flag variables to determine which exit path to take.

---

## Inductive Definition

For every $n \geq 1$, the [[Class of Charts|class]] of $\text{BJ}_n$-charts is the smallest class defined inductively as follows.

**Base cases.** Any [[Chart Action|action]] is a $\text{BJ}_n$-chart.

**Inductive cases.** If $G_1, G_2, \ldots, G_i$ are $\text{BJ}_n$-charts and $p_1, p_2, \ldots, p_i$ are [[Chart Predicate|predicates]], then:

- $\text{SEQUENCE}(G_1, G_2)$ is a $\text{BJ}_n$-chart
- $\text{IF-THEN-ELSE}(p_1, G_1, G_2)$ is a $\text{BJ}_n$-chart
- $\Omega_i(q_1, G_1, q_2, G_2, \ldots, q_i, G_i)$ is a $\text{BJ}_n$-chart for $i \leq n$, where $q_j \in \{p_j, \neg p_j\}$

---

## The Omega Construct

$\Omega_i(q_1, G_1, q_2, G_2, \ldots, q_i, G_i)$ executes as:

1. Evaluate predicates $q_1, q_2, \ldots, q_i$ in sequence
2. If $q_j$ is true, execute $G_j$ and exit to continuation $j$
3. If all predicates are false, loop back

The $\Omega$ construct with $i$ exit conditions requires a program counter `pc` variable:

```
pc := 0
while pc == 0 do
	if q_1 then { execute G_1; pc := 1 }
	else if q_2 then { execute G_2; pc := 2 }
	else if q_3 then { execute G_3; pc := 3 }
	...
	else if q_i then { execute G_i; pc := i }
end

if pc == 1 then [continuation 1]
else if pc == 2 then [continuation 2]
else if pc == 3 then [continuation 3]
...
else if pc == i then [continuation i]
```

The `exit_code` variable stores "which exit was taken" as data.

---

## Relationship to D-Charts

$\text{D-charts} \equiv_w \text{BJ}_1\text{-charts}$

BJ_1-charts (loops with at most one exit condition) are equivalent to D-charts (standard `while` loops). Both represent the pure [[SESE Region|SESE]] discipline.