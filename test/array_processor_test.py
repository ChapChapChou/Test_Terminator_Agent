import pytest
from src.array_processor import processArray

# Test case for sum operation
def test_sum():
    assert processArray([1, 2, 3], 'sum') == 6, "Should return the sum of all elements"

# Test case for average operation
def test_average():
    assert processArray([1, 2, 3, 4], 'average') == 2.5, "Should return the average of all elements"

# Test case for max operation
def test_max():
    assert processArray([1, 2, 3, 4, 5], 'max') == 5, "Should return the maximum element"

# Test case for min operation
def test_min():
    assert processArray([1, 2, 3, 4, 5], 'min') == 1, "Should return the minimum element"

# Test case for get operation with valid index
def test_get_valid_index():
    assert processArray([10, 20, 30, 40, 50], 'get', 2) == 30, "Should return the element at the specified index"

# Test case for get operation with invalid index (out of bounds)
def test_get_invalid_index():
    with pytest.raises(RangeError):
        processArray([10, 20, 30, 40, 50], 'get', 10)

# Test case for unsupported operation
def test_unsupported_operation():
    with pytest.raises(Error):
        processArray([1, 2, 3], 'multiply')

# Test case for empty array
def test_empty_array():
    with pytest.raises(Error):
        processArray([], 'sum')

# Test case for null array
def test_null_array():
    with pytest.raises(Error):
        processArray(None, 'sum')

# Test case for sum operation with negative numbers
def test_sum_negative_numbers():
    assert processArray([-1, -2, -3], 'sum') == -6, "Should return the sum of all negative elements"

# Test case for average operation with mixed positive and negative numbers
def test_average_mixed_numbers():
    assert processArray([-1, 1, -2, 2], 'average') == 0, "Should return the average of mixed positive and negative elements"

# Test case for max operation with all negative numbers
def test_max_negative_numbers():
    assert processArray([-10, -20, -30], 'max') == -10, "Should return the maximum element among negative numbers"

# Test case for min operation with all negative numbers
def test_min_negative_numbers():
    assert processArray([-1, -2, -3, -4], 'min') == -4, "Should return the minimum element among negative numbers"