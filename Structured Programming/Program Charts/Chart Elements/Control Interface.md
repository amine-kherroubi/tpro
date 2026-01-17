# Control Interface

The **control interface** of a construct specifies its entry and exit points—the syntactic points where control enters and leaves the construct.

---

## Standard Interfaces

Structured constructs have fixed control interfaces:

- **Sequencing**: One entry (into first component), one exit (from last component)
- **Selection**: One entry (the test), one exit (after reconvergence)
- **Iteration**: One entry (the condition), one exit (after termination)

---

## SESE Property

Constructs with one entry and one exit have the [[SESE Region|SESE property]]. The standard structured constructs all maintain SESE.

---

## Extended Interfaces

[[Multi-Level Exit|Multi-level exits]] extend the control interface by allowing exits at different structural depths, while maintaining the constraint that control decisions remain structural rather than encoded in variables.