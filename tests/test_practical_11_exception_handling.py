"""Tests for Practical 11 – Exception Handling."""

import runpy

from tests.conftest import PRACTICALS_DIR


def test_script_runs_without_error(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_11_exception_handling.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Error:" in captured.out


def test_zero_division_caught(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_11_exception_handling.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Error: Cannot divide by zero." in captured.out


def test_value_error_caught(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_11_exception_handling.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Error: Invalid conversion to integer." in captured.out


def test_index_error_caught(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_11_exception_handling.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Error: Index out of range." in captured.out


def test_file_not_found_caught(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_11_exception_handling.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Error: File not found." in captured.out


def test_custom_raise_caught(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_11_exception_handling.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Custom Error: Age cannot be negative." in captured.out


def test_finally_block_executes(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_11_exception_handling.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Execution complete." in captured.out


def test_division_by_zero_in_multi_except(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_11_exception_handling.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    # x = int("0") → 0, 100/0 → ZeroDivisionError
    assert "Error: Division by zero." in captured.out
