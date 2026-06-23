"""Practical 8 - User-Defined Functions.

Demonstrates function definition; uses shared factorial and area helpers.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared_utils import factorial, area_rectangle


# --- Basic greeting function ---
def greet(name):
    print("Hello,", name)


greet("Madhuri")
greet("Aarti")


# --- Addition function ---
def add(a, b):
    return a + b


result = add(12, 8)
print("Student: Rohit | Sum:", result)


# --- Even check ---
def is_even(n):
    return n % 2 == 0


print("Student: Tejas")
print("Is 14 even?", is_even(14))
print("Is 7 even?", is_even(7))

# --- Factorial using shared utility ---
print("Student: Reema")
print("Factorial of 5:", factorial(5))
print("Factorial of 7:", factorial(7))

# --- Area using shared utility ---
print("Area of 5x3 rectangle:", area_rectangle(5, 3))


# --- Default arguments ---
def student_info(name, city="Pune", course="BCA"):
    print(f"Name: {name}, City: {city}, Course: {course}")


student_info("Madhuri")
student_info("Aarti", "Mumbai", "BSc")
