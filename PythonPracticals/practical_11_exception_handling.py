"""Practical 11 - Exception Handling.

Demonstrates try/except/finally patterns.  The grading module's
``categorize_age`` already validates input, showing how shared utilities
reduce the need for manual exception patterns.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared_utils import categorize_age

# --- ZeroDivisionError ---
print("Student: Ritu")
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Error: Cannot divide by zero.")

# --- ValueError ---
print("Student: Kiran")
try:
    num = int("hello")
except ValueError:
    print("Error: Invalid conversion to integer.")

# --- IndexError ---
print("Student: Naina")
try:
    marks = [90, 85, 78]
    print(marks[5])
except IndexError:
    print("Error: Index out of range.")

# --- Multiple exceptions with finally ---
print("Student: Gaurav")
try:
    x = int("0")
    result = 100 / x
    print("Result:", result)
except ZeroDivisionError:
    print("Error: Division by zero.")
except ValueError:
    print("Error: Please enter a valid number.")
finally:
    print("Execution complete.")

# --- FileNotFoundError ---
print("Student: Mohit")
try:
    with open("notfound.txt", "r") as f:
        f.read()
except FileNotFoundError:
    print("Error: File not found.")

# --- raise / shared utility validation ---
print("Student: Pallavi")
age = -5
result = categorize_age(age)
print(f"Age {age} -> {result}")
