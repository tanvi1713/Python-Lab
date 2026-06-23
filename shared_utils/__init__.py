"""Shared utilities for Python Lab practicals.

This package extracts common patterns duplicated across student submissions
into reusable modules:

- grading:    Grade calculation and age categorization
- file_ops:   File read / write / append helpers
- csv_ops:    CSV create / read / write / filter helpers
- math_ops:   Factorial, area, and common math helpers
- input_helpers: Safe input with type validation
"""

from shared_utils.grading import calculate_grade, categorize_age
from shared_utils.file_ops import write_lines, read_file, read_lines, append_lines
from shared_utils.csv_ops import (
    create_sample_csv,
    read_csv_rows,
    read_csv_dicts,
    filter_csv,
    write_csv_rows,
    write_csv_dicts,
    append_csv_row,
)
from shared_utils.math_ops import factorial, area_rectangle, fibonacci
from shared_utils.input_helpers import get_integer, get_float

__all__ = [
    "calculate_grade",
    "categorize_age",
    "write_lines",
    "read_file",
    "read_lines",
    "append_lines",
    "create_sample_csv",
    "read_csv_rows",
    "read_csv_dicts",
    "filter_csv",
    "write_csv_rows",
    "write_csv_dicts",
    "append_csv_row",
    "factorial",
    "area_rectangle",
    "fibonacci",
    "get_integer",
    "get_float",
]
