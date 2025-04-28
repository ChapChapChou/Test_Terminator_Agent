/**
 * Process an array of numbers based on different operations
 * @param {number[]} numbers - Array of numbers to process
 * @param {string} operation - Operation to perform: 'sum', 'average', 'max', 'min', 'get'
 * @param {number} [index] - Index for 'get' operation
 * @returns {number} Result of the operation
 * @throws {Error} If operation is not supported or array is empty
 * @throws {RangeError} If index is out of bounds
 */
function processArray(numbers, operation, index) {
    // Check if array is empty
    if (!numbers || numbers.length === 0) {
        throw new Error("Array is empty");
    }

    // Different logical branches based on operation
    switch (operation) {
        case 'sum':
            return numbers.reduce((sum, num) => sum + num, 0);
            
        case 'average':
            const sum = numbers.reduce((sum, num) => sum + num, 0);
            return sum / numbers.length;
            
        case 'max':
            return Math.max(...numbers);
            
        case 'min':
            return Math.min(...numbers);
            
        case 'get':
            // This will throw RangeError if index is out of bounds
            if (index < 0 || index >= numbers.length) {
                throw new RangeError(`Index ${index} is out of bounds for array of length ${numbers.length}`);
            }
            return numbers[index];
            
        default:
            throw new Error(`Unsupported operation: ${operation}`);
    }
}

// Example usage
function main() {
    const numbers = [1, 2, 3, 4, 5];
    
    try {
        // Normal operations
        console.log("Sum:", processArray(numbers, 'sum'));
        console.log("Average:", processArray(numbers, 'average'));
        console.log("Max:", processArray(numbers, 'max'));
        console.log("Min:", processArray(numbers, 'min'));
        
        // Valid index
        console.log("Element at index 2:", processArray(numbers, 'get', 2));
        
        // This will throw RangeError
        console.log("Element at index 10:", processArray(numbers, 'get', 10));
    } catch (error) {
        if (error instanceof RangeError) {
            console.error("Range Error:", error.message);
        } else {
            console.error("Error:", error.message);
        }
    }
    
    // This will throw Error
    try {
        processArray([], 'sum');
    } catch (error) {
        console.error("Error:", error.message);
    }
}

// Run the program
main(); 




/*
这个 JavaScript 程序包含多个逻辑分支和一个数组越界错误：
主要逻辑分支（使用 switch 语句）：
求和分支 (case 'sum')
平均值分支 (case 'average')
最大值分支 (case 'max')
最小值分支 (case 'min')
获取元素分支 (case 'get')
默认错误分支 (default)
错误处理分支：
空数组检查 (if (!numbers || numbers.length === 0))
数组越界检查 (if (index < 0 || index >= numbers.length))
错误类型区分 (if (error instanceof RangeError))
包含的错误：
数组越界错误（RangeError）
空数组错误（Error）
不支持的操作错误（Error）
*/