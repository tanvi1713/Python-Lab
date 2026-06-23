"""Grade calculation and age categorization.

Extracted from the duplicated if/elif chains found across 30+ student
submissions in practical 5 (Conditional Statements).
"""

from typing import List, Tuple


# Default thresholds used by the majority of student submissions.
_DEFAULT_GRADE_SCALE: List[Tuple[int, str]] = [
    (90, "O (Outstanding)"),
    (75, "A+ (Excellent)"),
    (60, "A (Very Good)"),
    (50, "B (Good)"),
    (40, "C (Pass)"),
]


def calculate_grade(
    marks: int,
    scale: List[Tuple[int, str]] = _DEFAULT_GRADE_SCALE,
    fail_label: str = "F (Fail)",
) -> str:
    """Return a grade string for the given marks.

    Parameters
    ----------
    marks : int
        Numeric score (0-100).
    scale : list of (threshold, label) pairs
        Evaluated top-down; first match wins.  Must be sorted descending by
        threshold.
    fail_label : str
        Label returned when *marks* is below every threshold.

    >>> calculate_grade(92)
    'O (Outstanding)'
    >>> calculate_grade(55)
    'B (Good)'
    >>> calculate_grade(30)
    'F (Fail)'
    """
    for threshold, label in scale:
        if marks >= threshold:
            return label
    return fail_label


_DEFAULT_AGE_BRACKETS: List[Tuple[int, str]] = [
    (60, "Senior Citizen"),
    (18, "Adult"),
    (13, "Teenager"),
    (0, "Child"),
]


def categorize_age(
    age: int,
    brackets: List[Tuple[int, str]] = _DEFAULT_AGE_BRACKETS,
) -> str:
    """Return an age-category string.

    Parameters
    ----------
    age : int
        Age in years.
    brackets : list of (lower_bound, label) pairs
        Evaluated top-down; first bracket whose lower bound <= age wins.
        Must be sorted descending by lower_bound.

    >>> categorize_age(5)
    'Child'
    >>> categorize_age(25)
    'Adult'
    >>> categorize_age(-1)
    'Invalid age entered!'
    """
    if age < 0:
        return "Invalid age entered!"
    for lower_bound, label in brackets:
        if age >= lower_bound:
            return label
    return "Unknown"
