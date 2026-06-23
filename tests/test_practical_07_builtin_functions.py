"""Tests for Practical 07 – Built-in Functions."""

import runpy

from tests.conftest import PRACTICALS_DIR


def test_script_runs_without_error(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_07_builtin_functions.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Length:" in captured.out


def test_list_functions(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_07_builtin_functions.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    numbers = [45, 12, 78, 34, 89, 23]
    assert f"Length: {len(numbers)}" in captured.out
    assert f"Maximum: {max(numbers)}" in captured.out
    assert f"Minimum: {min(numbers)}" in captured.out
    assert f"Sum: {sum(numbers)}" in captured.out


def test_math_functions(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_07_builtin_functions.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Absolute value of -9: 9" in captured.out
    assert "Power 2^8: 256" in captured.out
    assert "Round 3.7654: 3.77" in captured.out


def test_string_functions(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_07_builtin_functions.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Upper: NANDINI" in captured.out
    assert "Length of name: 7" in captured.out


def test_type_conversions(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_07_builtin_functions.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "int('42'): 42" in captured.out
    assert "float('3.14'): 3.14" in captured.out
    assert "str(100): 100" in captured.out
    assert "bool(0): False" in captured.out
    assert "bool(1): True" in captured.out
