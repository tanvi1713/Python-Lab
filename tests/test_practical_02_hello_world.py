"""Tests for Practical 02 – Hello World Program."""

import runpy

from tests.conftest import PRACTICALS_DIR


def test_script_runs_without_error(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_02_hello_world.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Hello, World!" in captured.out


def test_output_contains_formatted_string(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_02_hello_world.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Hello, my name is Priya Desai" in captured.out
    assert "Pune" in captured.out


def test_output_contains_age(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_02_hello_world.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "20" in captured.out


def test_welcome_message(capsys):
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_02_hello_world.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Welcome to Python Programming!" in captured.out
