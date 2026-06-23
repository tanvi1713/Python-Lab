"""CSV create / read / write / filter helpers.

Extracted from the duplicated CSV patterns found in 30+ student submissions
in practicals 12 (Read CSV) and 13 (Write CSV).
"""

import csv
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Union


def create_sample_csv(
    filepath: Union[str, Path],
    headers: List[str],
    rows: List[List[Any]],
) -> None:
    """Create a CSV with *headers* and *rows*.

    >>> create_sample_csv(
    ...     "students.csv",
    ...     ["Name", "Roll", "Branch", "Marks"],
    ...     [["Alice", 101, "CS", 85], ["Bob", 102, "IT", 90]],
    ... )
    """
    filepath = Path(filepath)
    with filepath.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)
        writer.writerows(rows)


def read_csv_rows(filepath: Union[str, Path]) -> List[List[str]]:
    """Return all rows (including the header) as lists of strings.

    >>> rows = read_csv_rows("students.csv")
    >>> rows[0]
    ['Name', 'Roll', 'Branch', 'Marks']
    """
    filepath = Path(filepath)
    with filepath.open("r", newline="", encoding="utf-8") as fh:
        return list(csv.reader(fh))


def read_csv_dicts(filepath: Union[str, Path]) -> List[Dict[str, str]]:
    """Return all data rows as ordered dicts keyed by column header.

    >>> dicts = read_csv_dicts("students.csv")
    >>> dicts[0]["Name"]
    'Alice'
    """
    filepath = Path(filepath)
    with filepath.open("r", newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def filter_csv(
    filepath: Union[str, Path],
    predicate: Callable[[Dict[str, str]], bool],
) -> List[Dict[str, str]]:
    """Return rows from *filepath* for which *predicate* returns True.

    >>> high = filter_csv("students.csv", lambda r: int(r["Marks"]) >= 88)
    """
    return [row for row in read_csv_dicts(filepath) if predicate(row)]


def write_csv_rows(
    filepath: Union[str, Path],
    headers: List[str],
    rows: List[List[Any]],
) -> None:
    """Write *rows* with *headers* to a new CSV file (alias for create_sample_csv)."""
    create_sample_csv(filepath, headers, rows)


def write_csv_dicts(
    filepath: Union[str, Path],
    fieldnames: List[str],
    rows: List[Dict[str, Any]],
) -> None:
    """Write a list of dicts to a CSV using :class:`csv.DictWriter`.

    >>> write_csv_dicts(
    ...     "subjects.csv",
    ...     ["Subject", "Code", "Credits"],
    ...     [{"Subject": "Python", "Code": "CS301", "Credits": 3}],
    ... )
    """
    filepath = Path(filepath)
    with filepath.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_csv_row(
    filepath: Union[str, Path],
    row: List[Any],
) -> None:
    """Append a single row to an existing CSV file.

    >>> append_csv_row("students.csv", ["Eve", 105, "MECH", 88])
    """
    filepath = Path(filepath)
    with filepath.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(row)
