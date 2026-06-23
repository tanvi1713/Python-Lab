"""Tests for Practical 05 – Conditional Statements."""

import runpy

from tests.conftest import PRACTICALS_DIR


def test_script_runs_without_error(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_05_if_statements.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Result: Pass" in captured.out


def test_pass_fail_logic(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_05_if_statements.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    # marks = 75 >= 35 → Pass
    assert "Result: Pass" in captured.out


def test_first_class_logic(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_05_if_statements.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    # score = 82 >= 60 → First Class
    assert "Grade: First Class" in captured.out


def test_voting_eligibility(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_05_if_statements.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    # age = 17 < 18 → Not eligible
    assert "Not eligible to vote" in captured.out


def test_grade_classification(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_05_if_statements.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    # percentage = 88 → 80 <= 88 < 90 → Grade A
    assert "Grade: A" in captured.out


def test_positive_negative_zero(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_05_if_statements.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    # num = -5 → Negative
    assert "Negative Number" in captured.out
