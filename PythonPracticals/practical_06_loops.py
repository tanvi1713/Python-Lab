"""Practical 6 - Loops (for, while, nested).

Demonstrates loops; uses shared fibonacci utility for the while-loop example.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared_utils import fibonacci

# --- for loop: counting ---
print("Student: Pooja")
for i in range(1, 6):
    print("Count:", i)

# --- for loop: iterating a list ---
fruits = ["Mango", "Banana", "Guava", "Papaya"]
print("Student: Arjun")
for fruit in fruits:
    print("Fruit:", fruit)

# --- while loop via shared fibonacci ---
print("Student: Deepak")
fib = fibonacci(8)
print("Fibonacci (first 8):", fib)

# --- nested loop: multiplication table ---
print("Student: Rohit")
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} x {j} = {i*j}")

# --- sum using loop ---
total = 0
print("Student: Pooja")
for i in range(1, 11):
    total += i
print("Sum of 1 to 10:", total)

# --- even numbers ---
print("Student: Arjun")
for i in range(2, 21, 2):
    print(i, end=" ")
print()
