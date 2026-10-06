# qt-bounded-counter

Choices where the prompt is ambiguous: where the prompt only says the count "must stay in [0, max]", I chose **saturating (clamping) semantics** over raising — `add` past max leaves the count at max and `remove` past 0 leaves it at 0, so the invariant can never be violated by any call; both methods return the new count. `count` is a read-only property, a negative `max` raises `ValueError`, and a negative `n` moves the count in the opposite direction, still clamped.

Checked with assertions for basic add/remove, saturation at both bounds, `max=0`, negative `n`, rejection of a negative `max`, and that `count` cannot be assigned to — all pass (Python 3, stdlib only).
