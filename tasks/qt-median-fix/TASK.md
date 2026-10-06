# qt-median-fix

A short coding task (part of a quality check: same prompt other models got).

## Prompt

Fix this buggy median function so it returns the average of the two middle elements for even-length lists (float), the middle element for odd-length lists (int), and None for an empty list. 

def median(data):
    s = sorted(data)
    n = len(s)
    if n == 0: return None
    return s[n // 2]

## Deliver

- `results/qt-median-fix/solution.py`: the code only, runnable as a module (Python 3, standard library).
- `results/qt-median-fix/RESULT.md`: one or two lines on the choices you made where the prompt is ambiguous, and how you checked it.
