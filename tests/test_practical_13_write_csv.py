"""Tests for Practical 13 – Write CSV File.

Runs in a temporary directory to avoid polluting the repo.
"""

import csv
import runpy

from tests.conftest import PRACTICALS_DIR


def test_script_runs_without_error(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_13_write_csv.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "CSV file written successfully" in captured.out


def test_csv_file_created(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_13_write_csv.py", run_name="__main__"
    )
    assert (tmp_path / "employees.csv").exists()


def test_csv_has_correct_headers(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_13_write_csv.py", run_name="__main__"
    )
    with open(tmp_path / "employees.csv") as f:
        reader = csv.reader(f)
        header = next(reader)
    assert header == ["Name", "Department", "Salary", "City"]


def test_csv_has_correct_row_count(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_13_write_csv.py", run_name="__main__"
    )
    with open(tmp_path / "employees.csv") as f:
        reader = csv.reader(f)
        rows = list(reader)
    # 1 header + 6 original + 1 appended = 8
    assert len(rows) == 8


def test_appended_record(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_13_write_csv.py", run_name="__main__"
    )
    content = (tmp_path / "employees.csv").read_text()
    assert "Rahul Kulkarni" in content


def test_new_record_appended_message(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_13_write_csv.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "New record appended" in captured.out


def test_it_department_filter(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_13_write_csv.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    assert "IT Department Employees:" in captured.out
    assert "Aishwarya Desai" in captured.out
    assert "Nilima Jadhav" in captured.out


def test_salary_statistics(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(
        f"{PRACTICALS_DIR}/practical_13_write_csv.py", run_name="__main__"
    )
    captured = capsys.readouterr()
    salaries = [45000, 38000, 52000, 47000, 35000, 55000, 49000]
    assert f"Total Salary: {sum(salaries)}" in captured.out
    assert f"Average Salary: {sum(salaries)/len(salaries)}" in captured.out
