# qt-median-fix

The bug was that the original always returned `s[n // 2]` — the upper-middle element — so even-length lists never got the average of the two middle elements. The fix branches on parity: odd length returns the middle element unchanged (int in, int out), even length returns `(s[mid - 1] + s[mid]) / 2`, where Python 3 true division guarantees a float even when the average is whole (e.g. `[1, 3]` → `2.0`). Input is sorted on a copy, so the caller's list is not mutated.

Checked with assertions for empty, single, odd, even (including unsorted, negative and whole-average cases), type checks (`int` vs `float`), non-mutation of the input, and cross-checked against `statistics.median` — all pass.
