def median(data):
    """Return the median of a sequence of numbers.

    Empty input returns None. For an odd number of elements, returns
    the middle element itself (so int input yields an int). For an even
    number of elements, returns the average of the two middle elements
    as a float. The input is not mutated.
    """
    s = sorted(data)
    n = len(s)
    if n == 0:
        return None
    mid = n // 2
    if n % 2 == 1:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2
