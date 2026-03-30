# Interference Classification

## Purpose

Interference classification maps a numerical interference score to a qualitative severity label.

This makes diagnostic output easier to interpret while preserving the underlying numeric value.

---

## Definition

Given an interference score `s`:

```text
LOW     if s < 0.5
MEDIUM  if 0.5 ≤ s < 1.0
HIGH    if s ≥ 1.0

---

Interpretation
LOW means weak boundary pressure
MEDIUM means moderate boundary pressure
HIGH means strong rupture pressure

---

## Role in CFM

This classification is diagnostic only.

It does not affect:
- admissibility
- core transitions
- core state

It only enriches interpretation.

