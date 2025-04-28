def calculate(a: float, b: float, operation: str) -> float:
    """
    Perform basic arithmetic operations on two numbers.
    
    Args:
        a: First number
        b: Second number
        operation: One of '+', '-', '*', '/'
    
    Returns:
        Result of the calculation
    
    Raises:
        ValueError: If operation is not supported
        ZeroDivisionError: If dividing by zero
    """
    if operation == '+':
        return a + b
    elif operation == '-':
        return a - b
    elif operation == '*':
        return a * b
    elif operation == '/':
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b
    else:
        raise ValueError(f"Unsupported operation: {operation}")

def main():
    # Example usage
    try:
        result = calculate(10, 5, '+')
        print(f"10 + 5 = {result}")
        
        result = calculate(10, 5, '-')
        print(f"10 - 5 = {result}")
        
        result = calculate(10, 5, '*')
        print(f"10 * 5 = {result}")
        
        result = calculate(10, 5, '/')
        print(f"10 / 5 = {result}")
        
        # This will raise an error
        result = calculate(10, 0, '/')
    except ZeroDivisionError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 