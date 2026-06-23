"""Tests for Practical 10 – File Handling.

Runs the script in a temporary directory to avoid polluting the repo.
"""

import os
import runpy
import tempfile

from tests.conftest import PRACTICALS_DIR


def test_script_creates_and_reads_file(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_10_file_handling.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "File written successfully" in captured.out
    assert "Data appended" in captured.out
    assert "File exists." in captured.out


def test_file_content_is_correct(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_10_file_handling.py", run_name="__main__"
    )
    filepath = tmp_path / "vijay_data.txt"
    assert filepath.exists()
    content = filepath.read_text()
    assert "Name: Vijay Shinde" in content
    assert "City: Aurangabad" in content
    assert "Course: BCA" in content
    assert "Marks: 88" in content


def test_file_has_four_lines(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_10_file_handling.py", run_name="__main__"
    )
    filepath = tmp_path / "vijay_data.txt"
    lines = filepath.read_text().strip().splitlines()
    assert len(lines) == 4


def test_readlines_output(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_10_file_handling.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Vijay Shinde" in captured.out
    assert "Marks: 88" in captured.out
