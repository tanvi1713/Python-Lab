"""Common math helpers.

Extracted from the duplicated patterns found in practicals 6 (Loops),
7 (Built-in Functions), and 8 (User-Defined Functions).
"""

from typing import List


def factorial(n: int) -> int:
    """Return n! using recursion.

    >>> factorial(5)
    120
    >>> factorial(0)
    1
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def area_rectangle(length: float, width: float) -> float:
    """Return the area of a rectangle.

    >>> area_rectangle(5, 3)
    15
    """
    return length * width


def fibonacci(count: int) -> List[int]:
    """Return the first *count* Fibonacci numbers.

    >>> fibonacci(8)
    [0, 1, 1, 2, 3, 5, 8, 13]
    """
    if count <= 0:
        return []
    sequence: List[int] = []
    a, b = 0, 1
    for _ in range(count):
        sequence.append(a)
        a, b = b, a + b
    return sequence
