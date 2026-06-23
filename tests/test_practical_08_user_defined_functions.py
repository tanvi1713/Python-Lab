"""Tests for Practical 08 – User-Defined Functions.

This module has real functions (add, is_even, factorial, greet, student_info)
that can be tested directly by importing them.
"""

import importlib
import runpy
import sys
from unittest.mock import patch

from tests.conftest import PRACTICALS_DIR


def _import_practical_08():
    """Import practical_08 while suppressing top-level print side effects."""
    module_path = f"{PRACTICALS_DIR}/practical_08_user_defined_functions.py"
    with patch("builtins.print"):
        namespace = runpy.run_path(module_path, run_name="__main__")
    return namespace


class TestGreet:
    def test_greet_prints_name(self, capsys):
        ns = _import_practical_08()
        greet = ns["greet"]
        greet("TestUser")
        captured = capsys.readouterr()
        assert "Hello, TestUser" in captured.out

    def test_greet_prints_different_name(self, capsys):
        ns = _import_practical_08()
        greet = ns["greet"]
        greet("Alice")
        captured = capsys.readouterr()
        assert "Hello, Alice" in captured.out


class TestAdd:
    def test_add_positive_numbers(self):
        ns = _import_practical_08()
        add = ns["add"]
        assert add(12, 8) == 20

    def test_add_negative_numbers(self):
        ns = _import_practical_08()
        add = ns["add"]
        assert add(-3, -7) == -10

    def test_add_zero(self):
        ns = _import_practical_08()
        add = ns["add"]
        assert add(0, 0) == 0

    def test_add_mixed(self):
        ns = _import_practical_08()
        add = ns["add"]
        assert add(-5, 10) == 5

    def test_add_floats(self):
        ns = _import_practical_08()
        add = ns["add"]
        assert abs(add(1.5, 2.5) - 4.0) < 1e-9


class TestIsEven:
    def test_even_number(self):
        ns = _import_practical_08()
        is_even = ns["is_even"]
        assert is_even(14) is True

    def test_odd_number(self):
        ns = _import_practical_08()
        is_even = ns["is_even"]
        assert is_even(7) is False

    def test_zero_is_even(self):
        ns = _import_practical_08()
        is_even = ns["is_even"]
        assert is_even(0) is True

    def test_negative_even(self):
        ns = _import_practical_08()
        is_even = ns["is_even"]
        assert is_even(-4) is True

    def test_negative_odd(self):
        ns = _import_practical_08()
        is_even = ns["is_even"]
        assert is_even(-3) is False


class TestFactorial:
    def test_factorial_zero(self):
        ns = _import_practical_08()
        factorial = ns["factorial"]
        assert factorial(0) == 1

    def test_factorial_one(self):
        ns = _import_practical_08()
        factorial = ns["factorial"]
        assert factorial(1) == 1

    def test_factorial_five(self):
        ns = _import_practical_08()
        factorial = ns["factorial"]
        assert factorial(5) == 120

    def test_factorial_seven(self):
        ns = _import_practical_08()
        factorial = ns["factorial"]
        assert factorial(7) == 5040

    def test_factorial_ten(self):
        ns = _import_practical_08()
        factorial = ns["factorial"]
        assert factorial(10) == 3628800


class TestStudentInfo:
    def test_default_parameters(self, capsys):
        ns = _import_practical_08()
        student_info = ns["student_info"]
        student_info("Madhuri")
        captured = capsys.readouterr()
        assert "Madhuri" in captured.out
        assert "Pune" in captured.out
        assert "BCA" in captured.out

    def test_custom_parameters(self, capsys):
        ns = _import_practical_08()
        student_info = ns["student_info"]
        student_info("Aarti", "Mumbai", "BSc")
        captured = capsys.readouterr()
        assert "Aarti" in captured.out
        assert "Mumbai" in captured.out
        assert "BSc" in captured.out

    def test_partial_override(self, capsys):
        ns = _import_practical_08()
        student_info = ns["student_info"]
        student_info("Raj", "Delhi")
        captured = capsys.readouterr()
        assert "Raj" in captured.out
        assert "Delhi" in captured.out
        assert "BCA" in captured.out


class TestFullScriptExecution:
    def test_script_produces_expected_output(self, capsys):
        runpy.run_path(
            f"{PRACTICALS_DIR}/practical_08_user_defined_functions.py",
            run_name="__main__",
        )
        captured = capsys.readouterr()
        assert "Hello, Madhuri" in captured.out
        assert "Sum: 20" in captured.out
        assert "Is 14 even? True" in captured.out
        assert "Factorial of 5: 120" in captured.out
