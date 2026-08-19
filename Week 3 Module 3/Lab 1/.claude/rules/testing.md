# Testing Rules — NorthPeak Pricing Service

- Add a test for every behaviour change — new function, changed edge case, or
  bug fix.
- Name tests in sentence style describing the behaviour under test, e.g.
  `test_free_shipping_threshold`, not `test_shipping_1`.
- Cover the boundary value itself and both sides of it (e.g. just under and
  at `FREE_SHIPPING_THRESHOLD`).
- Every new public function needs at least one happy-path test and one
  invalid-input test (e.g. negative subtotal raises `ValueError`).
- `pytest -q` must pass before a change is considered done.
