"""Tests for Practical 03 – Variables and Data Types."""

import runpy

from tests.conftest import PRACTICALS_DIR


def test_script_runs_without_error(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_03_variables_datatypes.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Name:" in captured.out
    assert "Age:" in captured.out


def test_type_annotations_printed(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_03_variables_datatypes.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Type:" in captured.out
    assert "<class 'str'>" in captured.out
    assert "<class 'int'>" in captured.out
    assert "<class 'float'>" in captured.out
    assert "<class 'bool'>" in captured.out


def test_dynamic_typing(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_03_variables_datatypes.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Dynamic typing value: 3.14" in captured.out


def test_student_data_printed(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_03_variables_datatypes.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Vikram Nair" in captured.out
    assert "8.75" in captured.out
