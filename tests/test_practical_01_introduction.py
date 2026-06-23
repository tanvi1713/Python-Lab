"""Tests for Practical 01 – Introduction to Python and its Installation."""

import io
import runpy
import sys

from tests.conftest import PRACTICALS_DIR


def test_script_runs_without_error(capsys):
    """The script should execute and print system information."""
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_01_introduction.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Python Version:" in captured.out
    assert "Platform:" in captured.out
    assert "Machine:" in captured.out
    assert "Processor:" in captured.out
    assert "Python Implementation:" in captured.out


def test_output_contains_student_name(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_01_introduction.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Student:" in captured.out or "Rahul" in captured.out


def test_python_version_matches_runtime(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_01_introduction.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert sys.version.split()[0] in captured.out
