import pytest
from src.array_processor import processArray

# Test case for sum operation
def test_sum():
    assert processArray([1, 2, 3, 4, 5], 'sum') == 15, "Should return the sum of all elements"

# Test case for average operation
def test_average():
    assert processArray([1, 2, 3, 4, 5], 'average') == 3, "Should return the average of all elements"

# Test case for max operation
def test_max():
    assert processArray([1, 2, 3, 4, 5], 'max') == 5, "Should return the maximum element"

# Test case for min operation
def test_min():
    assert processArray([1, 2, 3, 4, 5], 'min') == 1, "Should return the minimum element"

# Test case for get operation with valid index
def test_get_valid_index():
    assert processArray([1, 2, 3, 4, 5], 'get', 2) == 3, "Should return the element at the specified index"

# Test case for get operation with invalid index (out of bounds)
def test_get_invalid_index():
    with pytest.raises(RangeError):
        processArray([1, 2, 3, 4, 5], 'get', 10)

# Test case for unsupported operation
def test_unsupported_operation():
    with pytest.raises(Error):
        processArray([1, 2, 3, 4, 5], 'multiply')

# Test case for empty array
def test_empty_array():
    with pytest.raises(Error):
        processArray([], 'sum')

# Test case for null array
def test_null_array():
    with pytest.raises(Error):
        processArray(None, 'sum')

# Test case for sum operation with negative numbers
def test_sum_with_negative_numbers():
    assert processArray([-1, -2, -3, -4, -5], 'sum') == -15, "Should return the sum of all elements including negative numbers"

# Test case for average operation with mixed numbers
def test_average_with_mixed_numbers():
    assert processArray([-1, 0, 1, 2, 3], 'average') == 1, "Should return the average of all elements including negative and positive numbers"

# Test case for max operation with all negative numbers
def test_max_with_all_negative_numbers():
    assert processArray([-1, -2, -3, -4, -5], 'max') == -1, "Should return the maximum element among negative numbers"

# Test case for min operation with all negative numbers
def test_min_with_all_negative_numbers():
    assert processArray([-1, -2, -3, -4, -5], 'min') == -5, "Should return the minimum element among negative numbers"