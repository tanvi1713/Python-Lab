"""Practical 10 - File Handling.

Demonstrates file I/O using shared file_ops utilities.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared_utils import write_lines, read_file, read_lines, append_lines

DATA_FILE = os.path.join(os.path.dirname(__file__), "vijay_data.txt")

# --- Write ---
write_lines(DATA_FILE, [
    "Name: Vijay Shinde\n",
    "City: Aurangabad\n",
    "Course: BCA\n",
])
print("Student: Vijay | File written successfully.")

# --- Read entire file ---
content = read_file(DATA_FILE)
print("Student: Sarika | File Content:\n", content)

# --- Append ---
append_lines(DATA_FILE, ["Marks: 88\n"])
print("Student: Omkar | Data appended.")

# --- Read lines ---
lines = read_lines(DATA_FILE, strip=True)
print("Student: Omkar | Lines in file:")
for line in lines:
    print(line)

# --- File existence check ---
print("File exists." if os.path.exists(DATA_FILE) else "File not found.")
