"""File read / write / append helpers.

Extracted from the duplicated open-write-read-append pattern found in 30+
student submissions in practical 10 (File Handling).
"""

from pathlib import Path
from typing import List, Optional, Union


def write_lines(
    filepath: Union[str, Path],
    lines: List[str],
    encoding: str = "utf-8",
) -> None:
    """Write *lines* to *filepath*, overwriting any existing content.

    Each element in *lines* is written as-is; append ``'\\n'`` yourself if
    needed.

    >>> write_lines("demo.txt", ["Name: Alice\\n", "Roll: 101\\n"])
    """
    filepath = Path(filepath)
    with filepath.open("w", encoding=encoding) as fh:
        fh.writelines(lines)


def read_file(
    filepath: Union[str, Path],
    encoding: str = "utf-8",
) -> str:
    """Return the entire content of *filepath* as a single string.

    >>> content = read_file("demo.txt")
    """
    filepath = Path(filepath)
    with filepath.open("r", encoding=encoding) as fh:
        return fh.read()


def read_lines(
    filepath: Union[str, Path],
    strip: bool = False,
    encoding: str = "utf-8",
) -> List[str]:
    """Return a list of lines from *filepath*.

    Parameters
    ----------
    strip : bool
        If True each line is ``.strip()``-ed before being returned.

    >>> read_lines("demo.txt", strip=True)
    ['Name: Alice', 'Roll: 101']
    """
    filepath = Path(filepath)
    with filepath.open("r", encoding=encoding) as fh:
        lines = fh.readlines()
    if strip:
        lines = [line.strip() for line in lines]
    return lines


def append_lines(
    filepath: Union[str, Path],
    lines: List[str],
    encoding: str = "utf-8",
) -> None:
    """Append *lines* to the end of *filepath*.

    >>> append_lines("demo.txt", ["City: Mumbai\\n"])
    """
    filepath = Path(filepath)
    with filepath.open("a", encoding=encoding) as fh:
        fh.writelines(lines)
