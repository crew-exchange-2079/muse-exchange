import csv
import io


def _cell_type(value):
    """Classify one non-empty cell as 'int', 'float' or 'str'."""
    try:
        int(value)
        return "int"
    except ValueError:
        pass
    try:
        float(value)
        return "float"
    except ValueError:
        return "str"


def _column_type(cell_types):
    """Combine the types of a column's non-empty cells into one label."""
    kinds = set(cell_types)
    if not kinds:
        return "str"
    if kinds == {"int"}:
        return "int"
    if kinds <= {"int", "float"}:
        return "float"
    if kinds == {"str"}:
        return "str"
    return "mixed"


def csv_summary(text):
    """Summarise a CSV string (header row plus data rows).

    Returns a dict with:
      rows      -- number of data rows (header not counted, blank
                   lines ignored)
      cols      -- number of columns (from the header)
      header    -- the header row as a list of strings
      col_types -- {column name: 'int'/'float'/'str'/'mixed'}

    A column is 'int' if every non-empty cell parses as an int,
    'float' if every non-empty cell is numeric and at least one is a
    float, 'str' if every non-empty cell is non-numeric, and 'mixed'
    otherwise. Empty cells are ignored when typing; a column with no
    non-empty cells is 'str'. Rows shorter than the header are padded
    with empty cells and extra cells are ignored.
    """
    reader = csv.reader(io.StringIO(text))
    rows = [row for row in reader if row]
    if not rows:
        return {"rows": 0, "cols": 0, "header": [], "col_types": {}}

    header = rows[0]
    data = rows[1:]
    cols = len(header)

    col_types = {}
    for i, name in enumerate(header):
        types = []
        for row in data:
            cell = row[i] if i < len(row) else ""
            if cell.strip() != "":
                types.append(_cell_type(cell.strip()))
        col_types[name] = _column_type(types)

    return {
        "rows": len(data),
        "cols": cols,
        "header": list(header),
        "col_types": col_types,
    }
