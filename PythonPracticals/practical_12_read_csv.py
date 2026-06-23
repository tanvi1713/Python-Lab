"""Practical 12 - Read CSV File.

Demonstrates CSV reading using shared csv_ops utilities.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared_utils import create_sample_csv, read_csv_rows, read_csv_dicts, filter_csv

CSV_PATH = os.path.join(os.path.dirname(__file__), "students.csv")

# --- Create sample CSV ---
create_sample_csv(
    CSV_PATH,
    ["Name", "Age", "City", "Marks"],
    [
        ["Amruta Jadhav", 21, "Aurangabad", 88],
        ["Rajesh Kulkarni", 22, "Pune", 76],
        ["Sunanda More", 20, "Nashik", 91],
        ["Ketan Pawar", 23, "Mumbai", 83],
        ["Varsha Shinde", 21, "Nagpur", 79],
    ],
)
print("CSV file created.")

# --- Read all rows ---
rows = read_csv_rows(CSV_PATH)
print("Student: Amruta | All Records:")
for row in rows:
    print(row)

# --- Read as dicts ---
dicts = read_csv_dicts(CSV_PATH)
print("Student: Rajesh | Name and Marks:")
for row in dicts:
    print(row["Name"], "->", row["Marks"])

# --- Filter + aggregate ---
marks = [int(r["Marks"]) for r in dicts]
print("Student: Sunanda | Max Marks:", max(marks))
print("Student: Ketan | Min Marks:", min(marks))
print("Student: Varsha | Average Marks:", sum(marks) / len(marks))

# --- Filter using predicate ---
high_scorers = filter_csv(CSV_PATH, lambda r: int(r["Marks"]) >= 85)
print("High scorers (>=85):")
for row in high_scorers:
    print(f"  {row['Name']} - {row['Marks']}")
