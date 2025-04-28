import pytest
from src.calculator import calculate

# Test case for addition
def test_addition():
    assert calculate(10, 5, '+') == 15, "Should return the sum of two numbers"

# Test case for subtraction
def test_subtraction():
    assert calculate(10, 5, '-') == 5, "Should return the difference of two numbers"

# Test case for multiplication
def test_multiplication():
    assert calculate(10, 5, '*') == 50, "Should return the product of two numbers"

# Test case for division
def test_division():
    assert calculate(10, 5, '/') == 2, "Should return the division of two numbers"

# Test case for division by zero
def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate(10, 0, '/')

# Test case for unsupported operation
def test_unsupported_operation():
    with pytest.raises(ValueError):
        calculate(10, 5, '%')

# Test case for floating point numbers
def test_floating_point():
    assert calculate(10.5, 4.5, '+') == 15, "Should handle floating point numbers correctly"

# Test case for negative numbers
def test_negative_numbers():
    assert calculate(-10, 5, '-') == -15, "Should handle negative numbers correctly"

# Test case for zero as input
def test_zero_input():
    assert calculate(0, 5, '+') == 5, "Should handle zero as an input correctly"

# Test case for large numbers
def test_large_numbers():
    assert calculate(1000000, 500000, '+') == 1500000, "Should handle large numbers correctly"