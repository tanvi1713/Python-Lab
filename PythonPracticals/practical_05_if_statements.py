"""Practical 5 - Conditional Statements.

Demonstrates if/elif/else using shared grading and age utilities.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared_utils import calculate_grade, categorize_age

# --- Grade Calculator using shared utility ---
marks = 75
print("Student: Karan")
print(f"Marks: {marks} -> Grade: {calculate_grade(marks)}")

score = 82
print("Student: Sneha")
print(f"Score: {score} -> Grade: {calculate_grade(score)}")

# --- Age Categorization using shared utility ---
age = 17
print("Student: Anjali")
print(f"Age: {age} -> {categorize_age(age)}")

# --- Grade ladder (same logic, custom scale) ---
percentage = 88
print("Student: Ramesh")
LETTER_SCALE = [
    (90, "O"),
    (80, "A"),
    (70, "B"),
    (60, "C"),
]
print(f"Percentage: {percentage} -> Grade: {calculate_grade(percentage, scale=LETTER_SCALE, fail_label='Fail')}")

# --- Simple positive/negative check (too small to extract) ---
num = -5
print("Student: Karan")
if num > 0:
    print("Positive Number")
elif num < 0:
    print("Negative Number")
else:
    print("Zero")
