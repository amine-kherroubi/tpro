# Control Flow as Data

**Control flow as data** is a technique where control decisions are encoded as values in variables rather than represented through graph structure. A variable stores the current control state, and assignments to this variable simulate control transfers.

---

## Transformation

Control flow as data transforms control edges into data updates, jumps to nodes into assignments to the [[Program Counter|program counter]], and arbitrary graphs into [[SESE Region|single-entry single-exit]] [[Chart Loop|loops]].