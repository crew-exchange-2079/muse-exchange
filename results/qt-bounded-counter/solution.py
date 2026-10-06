class BoundedCounter:
    """A counter whose count is kept within [0, max] at all times.

    add(n) increases the count by n and remove(n) decreases it by n;
    both saturate at the bounds instead of raising (adding past max
    leaves the count at max, removing past 0 leaves it at 0), and both
    return the new count. Passing a negative n to add/remove moves the
    count the other way, still clamped. A negative max is rejected.
    """

    def __init__(self, max):
        if max < 0:
            raise ValueError("max must be non-negative")
        self._max = max
        self._count = 0

    def add(self, n):
        self._count = min(self._max, max(0, self._count + n))
        return self._count

    def remove(self, n):
        self._count = min(self._max, max(0, self._count - n))
        return self._count

    @property
    def count(self):
        return self._count
