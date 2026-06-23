"""Tests for Practical 09 – Strings, Lists, Tuples & Sets."""

import runpy

from tests.conftest import PRACTICALS_DIR


def test_script_runs_without_error(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_09_strings_list_tuples_sets.py",
        run_name="__main__",
    )
    captured = capsys.readouterr()
    assert "Upper:" in captured.out


def test_string_operations(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_09_strings_list_tuples_sets.py",
        run_name="__main__",
    )
    captured = capsys.readouterr()
    assert "HARSHADA PATIL" in captured.out
    assert "harshada patil" in captured.out
    assert "Length: 14" in captured.out
    assert "Harshada Desai" in captured.out
    assert "Slice: Harshada" in captured.out
    assert "Find 'Patil': 9" in captured.out


def test_list_operations(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_09_strings_list_tuples_sets.py",
        run_name="__main__",
    )
    captured = capsys.readouterr()
    assert "Papaya" in captured.out
    assert "After remove:" in captured.out
    assert "Sorted:" in captured.out


def test_tuple_operations(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_09_strings_list_tuples_sets.py",
        run_name="__main__",
    )
    captured = capsys.readouterr()
    assert "Manasi" in captured.out
    assert "21" in captured.out
    assert "Nagpur" in captured.out
    assert "BSc" in captured.out


def test_set_operations(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_09_strings_list_tuples_sets.py",
        run_name="__main__",
    )
    captured = capsys.readouterr()
    assert "Union:" in captured.out
    assert "Intersection:" in captured.out
    assert "Difference:" in captured.out


def test_unique_cities(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_09_strings_list_tuples_sets.py",
        run_name="__main__",
    )
    captured = capsys.readouterr()
    assert "Unique Cities:" in captured.out
