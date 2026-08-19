# Style Rules — NorthPeak Pricing Service

- Keep public functions in `src/northpeak/` **pure** — no hidden state, no I/O,
  same inputs always produce the same outputs.
- **Validate inputs** at the boundary: reject negative money amounts with
  `ValueError` before doing any arithmetic on them.
- Every public function needs a one-line docstring describing what it returns.
- Use type hints on all public function signatures (e.g. `subtotal: float`).
- Money is float USD, rounded to 2 decimals only at the boundaries (return
  values), not in the middle of a calculation.
- Prefer small, single-purpose functions over one function that does
  discount + shipping + total in one block.
