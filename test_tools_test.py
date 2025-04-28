import os
import pytest
from test_tools import TestTools

@pytest.fixture
def test_tools():
    return TestTools()

@pytest.fixture
def sample_source_file(tmp_path):
    # Create a sample Python file for testing
    source_code = """
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
"""
    file_path = tmp_path / "calculator.py"
    with open(file_path, "w") as f:
        f.write(source_code)
    return str(file_path)

def test_scan_directory(test_tools, tmp_path):
    # Create some test files
    (tmp_path / "test1.py").write_text("")
    (tmp_path / "test2.json").write_text("")
    (tmp_path / "test3.txt").write_text("")  # This should be ignored
    
    files = test_tools.scan_directory(str(tmp_path))
    assert len(files) == 2
    assert any(f.endswith("test1.py") for f in files)
    assert any(f.endswith("test2.json") for f in files)

def test_analyze_code(test_tools, sample_source_file):
    analysis = test_tools.analyze_code(sample_source_file)
    assert "analysis" in analysis
    assert "source_file" in analysis
    assert analysis["source_file"] == sample_source_file
    assert "add" in analysis["analysis"].lower()
    assert "subtract" in analysis["analysis"].lower()

def test_generate_test(test_tools, sample_source_file):
    test_file = test_tools.generate_test(sample_source_file)
    assert os.path.exists(test_file)
    assert test_file.endswith("_test.py")
    
    # Read the generated test file
    with open(test_file, "r") as f:
        test_code = f.read()
    
    # Check if the test file contains expected content
    assert "import pytest" in test_code
    assert "def test_add" in test_code
    assert "def test_subtract" in test_code

def test_execute_test(test_tools, sample_source_file):
    # First generate a test file
    test_file = test_tools.generate_test(sample_source_file)
    
    # Execute the test
    results = test_tools.execute_test(test_file)
    assert isinstance(results, dict)
    assert "total" in results
    assert "passed" in results

def test_analyze_failures(test_tools):
    # Create a sample test result with failures
    test_results = {
        "total": 3,
        "passed": 1,
        "failed": 2,
        "failures": [
            {"test": "test_add", "error": "AssertionError: expected 3 but got 2"},
            {"test": "test_subtract", "error": "TypeError: unsupported operand type(s)"}
        ]
    }
    
    analysis = test_tools.analyze_failures(test_results)
    assert "analysis" in analysis
    assert "results" in analysis
    assert analysis["results"] == test_results

def test_generate_report(test_tools):
    # Create sample test results
    test_results = {
        "total": 3,
        "passed": 2,
        "failed": 1,
        "coverage": 85.5
    }
    
    report = test_tools.generate_report(test_results)
    assert isinstance(report, str)
    assert "total" in report.lower()
    assert "passed" in report.lower()
    assert "failed" in report.lower()
    assert "coverage" in report.lower()

def test_get_tools(test_tools):
    tools = test_tools.get_tools()
    assert len(tools) > 0
    assert all(hasattr(tool, "name") for tool in tools)
    assert all(hasattr(tool, "func") for tool in tools)
    assert all(hasattr(tool, "description") for tool in tools) 