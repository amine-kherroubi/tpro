# Kosaraju's Reducibility Hierarchy

For any $n \geq 1$, the [[Chart Class Reducibility|reducibility]] relations between [[Class of Charts|classes of charts]] can be organized as follows:

---

## BJ-Charts

- $\text{D-charts} \equiv_w \text{BJ}_1\text{-charts}$  
- $\text{BJ}_n\text{-charts} <_w \text{BJ}_{n+1}\text{-charts}$  
- $\text{BJ}_n\text{-charts} \leq_w \text{GP}_n\text{-charts}$  
- $\text{BJ}_n\text{-charts} <_w \text{RE}_2\text{-charts}$  

---

## RE-Charts

- $\bigcup_{n \geq 1} \text{BJ}_n\text{-charts} \leq_w \text{RE}_1\text{-charts}$  
- $\text{RE}_n\text{-charts} <_w \text{RE}_{n+1}\text{-charts}$  
- $\text{RE}_n\text{-charts} \leq_w \text{GRE}_n\text{-charts}$  
- $\text{RE}_n\text{-charts} \leq_w \text{DRE}_n\text{-charts}$  

---

## GRE-Charts

- $\text{GRE}_n\text{-charts} <_w \text{GRE}_{n+1}\text{-charts}$  

---

## DRE-Charts

- $\text{DRE}_n\text{-charts} \leq_w \text{DRE}_{n+1}\text{-charts}$  
- $\text{DRE}_n\text{-charts} \leq_w \text{GRE}_{n+1}\text{-charts}$  

---

## TD-Charts

- $\text{TD}_n\text{-charts} \leq_w \text{RE}_{3n}\text{-charts}$