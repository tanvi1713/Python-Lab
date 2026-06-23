"""Tests for Practical 04 – Operators."""

import runpy

from tests.conftest import PRACTICALS_DIR


def test_script_runs_without_error(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_04_operators.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Addition:" in captured.out
    assert "Subtraction:" in captured.out


def test_arithmetic_results(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_04_operators.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Addition: 19" in captured.out       # 15 + 4
    assert "Subtraction: 11" in captured.out    # 15 - 4
    assert "Multiplication: 60" in captured.out # 15 * 4
    assert "Floor Division: 3" in captured.out  # 15 // 4
    assert "Modulus: 3" in captured.out         # 15 % 4
    assert "Exponent: 50625" in captured.out    # 15 ** 4


def test_comparison_results(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_04_operators.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Greater Than: True" in captured.out
    assert "Less Than: False" in captured.out
    assert "Equal: False" in captured.out
    assert "Not Equal: True" in captured.out


def test_logical_results(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_04_operators.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "AND: False" in captured.out
    assert "OR: True" in captured.out
    assert "NOT p: False" in captured.out


def test_assignment_operators(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_04_operators.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    # n=7; +=3 → 10; -=2 → 8; *=2 → 16; //=3 → 5
    assert "After +=: 10" in captured.out
    assert "After -=: 8" in captured.out
    assert "After *=: 16" in captured.out
    assert "After //=: 5" in captured.out
