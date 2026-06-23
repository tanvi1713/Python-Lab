"""Safe input helpers with type validation.

Extracted from the duplicated int(input(...)) / try-except-ValueError
pattern found across most student practicals.
"""


def get_integer(prompt: str = "Enter an integer: ") -> int:
    """Prompt until the user provides a valid integer.

    >>> # (interactive) Enter an integer: abc
    >>> # Please enter a valid integer.
    >>> # Enter an integer: 42
    >>> # 42
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")


def get_float(prompt: str = "Enter a number: ") -> float:
    """Prompt until the user provides a valid float.

    >>> # (interactive) Enter a number: xyz
    >>> # Please enter a valid number.
    >>> # Enter a number: 3.14
    >>> # 3.14
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")
