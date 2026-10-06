# qt-csv-summary

Choices where the prompt is ambiguous: parsing uses the stdlib `csv` module, so quoted fields with commas work. `rows` counts data rows only (header excluded, blank lines ignored). Typing ignores empty cells: a column is `int` if all its non-empty cells parse as ints (signs allowed), `float` if all are numeric with at least one float (scientific notation counts as float), `str` if none are numeric — including a column with no values at all — and `mixed` when numeric and non-numeric cells combine. Rows shorter than the header are treated as having empty trailing cells; extra cells are ignored.

Checked with assertions covering all four type labels, signed ints, scientific notation, quoted commas, blank lines, short rows, a header-only CSV and empty input — all pass (Python 3, stdlib only).
