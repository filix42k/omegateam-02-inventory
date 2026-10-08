# Code smells in `pricing_legacy.py`

This is a read-only review of the instructor-provided baseline before refactoring.
Line numbers refer to that original file.

1. **Opaque tuple indexing and names (lines 17–28).** `t`, `i`, and `sub` hide the meaning of the calculation, while `i[1]` and `i[2]` make it easy to confuse quantity and unit price.
2. **Magic thresholds and rates (lines 24–27, 34–36, 42, 48, 52).** Bulk quantities, discount percentages, the point divisor, coupon rate, and tax are embedded in the calculation rather than named as policy.
3. **One function owns unrelated jobs (lines 12–56).** `calc` computes line totals, applies several discount types, mutates member points, applies tax and rounding, and records a log entry.
4. **Nested branching and repeated `!= None` checks (lines 30–48).** Membership and coupon logic are harder to scan than early exits or small named helpers.
5. **Hidden module state (lines 8–9, 31–36, 55).** Calling the same function can change `member_points` and `LOG`, so isolated tests need to reset both globals.
6. **Implicit wall-clock dependency (lines 43–47).** A `NEWYEAR` result changes over time when `today` is omitted, which makes an otherwise identical call nondeterministic.
7. **Unstated input and output shapes (line 12).** The tuple format and return type are only described in comments, so callers cannot see the contract from the signature.

The characterization suite records the current behavior, including discount order, the January-only coupon, negative-price clamping, rounding, points, and log side effects. The refactor is kept in a new module so both implementations remain available for comparison.
