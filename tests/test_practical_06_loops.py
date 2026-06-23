"""Tests for Practical 06 – Loops."""

import runpy

from tests.conftest import PRACTICALS_DIR


def test_script_runs_without_error(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_06_loops.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Count:" in captured.out


def test_for_loop_counts(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_06_loops.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    for i in range(1, 6):
        assert f"Count: {i}" in captured.out


def test_fruit_iteration(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_06_loops.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    for fruit in ["Mango", "Banana", "Guava", "Papaya"]:
        assert f"Fruit: {fruit}" in captured.out


def test_while_loop(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_06_loops.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    for i in range(1, 6):
        assert f"Number: {i}" in captured.out


def test_nested_loop_multiplication(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_06_loops.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "2 x 3 = 6" in captured.out
    assert "3 x 3 = 9" in captured.out


def test_sum_1_to_10(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_06_loops.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Sum of 1 to 10: 55" in captured.out


def test_even_numbers(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_06_loops.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    for i in range(2, 21, 2):
        assert str(i) in captured.out
