"""Practical 13 - Write CSV File.

Demonstrates CSV writing using shared csv_ops utilities.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared_utils import (
    write_csv_rows,
    write_csv_dicts,
    append_csv_row,
    read_csv_dicts,
    filter_csv,
)

CSV_PATH = os.path.join(os.path.dirname(__file__), "employees.csv")

# --- Write rows ---
write_csv_rows(
    CSV_PATH,
    ["Name", "Department", "Salary", "City"],
    [
        ["Aishwarya Desai", "IT", 45000, "Pune"],
        ["Rohit Mane", "HR", 38000, "Mumbai"],
        ["Meghna Patil", "Finance", 52000, "Aurangabad"],
        ["Nilima Jadhav", "IT", 47000, "Nashik"],
        ["Pravin Shinde", "Admin", 35000, "Nagpur"],
        ["Shital More", "Finance", 55000, "Pune"],
    ],
)
print("Student: Aishwarya | CSV file written successfully.")

# --- Append a row ---
append_csv_row(CSV_PATH, ["Rahul Kulkarni", "IT", 49000, "Mumbai"])
print("Student: Rohit | New record appended.")

# --- Read back ---
records = read_csv_dicts(CSV_PATH)
print("Student: Meghna | Employee Records:")
for row in records:
    print(row)

# --- Filter by department ---
it_employees = filter_csv(CSV_PATH, lambda r: r["Department"] == "IT")
print("Student: Nilima | IT Department Employees:")
for emp in it_employees:
    print(emp["Name"], "-", emp["Salary"])

# --- Aggregate salaries ---
salaries = [int(r["Salary"]) for r in records]
print("Student: Pravin | Total Salary:", sum(salaries))
print("Student: Shital | Average Salary:", sum(salaries) / len(salaries))
