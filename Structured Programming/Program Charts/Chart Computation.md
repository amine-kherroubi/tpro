# Chart Computation

A [[Flow Chart|chart]] executes according to the following rules:

1. [[Computational History|Control]] begins at the [[Chart Entry Point|IN point]] with the input value.
2. Each [[Chart Primitive|primitive]] executes one computational step.
3. [[Chart Action|Actions]] transform variable values and pass control along their [[Primitive Output Line|output line]].
4. [[Chart Predicate|Predicates]] evaluate conditions without modifying data and pass control along one of their output lines.
5. Execution continues until reaching the [[Chart Exit Point|OUT point]] or entering an infinite loop.