# qt-parse-record

Choices where the prompt is ambiguous: fields are split on every `|` with no stripping (whitespace is preserved), empty fields are kept as `""`, and a trailing pipe yields a final empty field (so `"a|b|"` has 3 fields); an empty line returns `{"field_0": ""}`. Key order relies on dict insertion order.

Checked with assertions covering the normal case, key order, empty middle field, trailing pipe, empty line, no delimiters, and whitespace preservation — all pass (Python 3, stdlib only).
