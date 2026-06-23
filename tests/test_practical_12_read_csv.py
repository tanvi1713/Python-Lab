"""Tests for Practical 12 – Read CSV File.

Runs in a temporary directory to avoid polluting the repo.
"""

import runpy

from tests.conftest import PRACTICALS_DIR


def test_script_runs_without_error(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_12_read_csv.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "CSV file created." in captured.out


def test_csv_file_created(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_12_read_csv.py", run_name="__main__"
    )
    assert (tmp_path / "students.csv").exists()


def test_csv_content(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_12_read_csv.py", run_name="__main__"
    )
    content = (tmp_path / "students.csv").read_text()
    assert "Amruta Jadhav" in content
    assert "Rajesh Kulkarni" in content
    assert "Sunanda More" in content


def test_all_records_printed(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_12_read_csv.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Amruta Jadhav" in captured.out
    assert "Rajesh Kulkarni" in captured.out


def test_name_and_marks_printed(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_12_read_csv.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "Rajesh Kulkarni -> 76" in captured.out


def test_statistics(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_12_read_csv.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    marks = [88, 76, 91, 83, 79]
    assert f"Max Marks: {max(marks)}" in captured.out
    assert f"Min Marks: {min(marks)}" in captured.out
    assert f"Average Marks: {sum(marks)/len(marks)}" in captured.out
