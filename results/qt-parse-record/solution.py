def parse_record(line):
    """Split a pipe-delimited string into an ordered dict.

    Returns {"field_0": ..., "field_1": ..., ...} with one entry per
    field, in order (dicts preserve insertion order). Empty fields are
    kept as empty strings, and a trailing pipe produces a final empty
    field. Whitespace is preserved as-is.
    """
    parts = line.split("|")
    return {f"field_{i}": part for i, part in enumerate(parts)}
