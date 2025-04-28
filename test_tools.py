import os
import json
from typing import List, Dict, Any
from langchain.tools import Tool
from langchain_community.tools import ShellTool
from langchain.chat_models import ChatOpenAI

class TestTools:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0
        )
        self.shell_tool = ShellTool()

    def scan_directory(self, directory: str) -> List[str]:
        """Recursively scan directory for Python, JSON, and JavaScript files."""
        source_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(('.py', '.json', '.js')):
                    source_files.append(os.path.join(root, file))
        return source_files

    def analyze_code(self, source_file: str) -> Dict[str, Any]:
        """Analyze source code to understand its structure and functionality."""
        with open(source_file, 'r') as f:
            source_code = f.read()
        
        prompt = f"""Analyze the following source code and provide a detailed understanding:
        {source_code}
        
        Please analyze:
        1. Code structure and organization
        2. Key functions and their purposes
        3. Dependencies and imports
        4. Error handling and edge cases
        5. Potential testing challenges
        
        Provide your analysis in a structured format."""
        
        response = self.llm.invoke(prompt)
        return {"analysis": response.content, "source_file": source_file}

    def generate_test(self, source_file: str, analysis: Dict[str, Any] = None) -> str:
        """Generate test cases for a source file using LLM."""
        with open(source_file, 'r') as f:
            source_code = f.read()
        
        context = ""
        if analysis:
            context = f"""Based on the following analysis:
            {analysis['analysis']}
            """
        
        prompt = f"""{context}
        Generate comprehensive test cases for the following source code:
        {source_code}
        
        Requirements:
        1. Create test cases that achieve 100% code coverage
        2. Include detailed comments explaining each test case
        3. Follow pytest conventions
        4. Consider edge cases and error conditions
        5. Test all public interfaces and key functionality
        6. Include setup and teardown as needed
        
        IMPORTANT: 
        - Only return the Python test code. Do not include any explanations or markdown formatting.
        - The code should start with import statements and end with the last test function.
        - Remember, All source code store in folder named src
        - Use relative imports, for example: from src.calculator import add
        - Make sure to import pytest at the beginning of the file
        """
        
        response = self.llm.invoke(prompt)
        test_code = response.content
        
        # Extract Python code from the response
        # Remove markdown code block markers if present
        test_code = test_code.replace('```python', '').replace('```', '')
        # Remove any leading/trailing whitespace
        test_code = test_code.strip()
        
        # Create test directory if it doesn't exist
        test_dir = "test"
        os.makedirs(test_dir, exist_ok=True)
        
        # Get the source file name without path and extension
        source_name = os.path.splitext(os.path.basename(source_file))[0]
        
        # Create test file path in test directory
        test_file = os.path.join(test_dir, f"{source_name}_test.py")
        
        # Save test file
        with open(test_file, 'w') as f:
            f.write(test_code)
        
        return test_file

    def execute_test(self, test_file: str) -> Dict[str, Any]:
        """Execute test cases using pytest and return results."""
        # Create a temporary JSON report file
        json_report_file = "test_report.json"
        
        # Run pytest with JSON report
        result = self.shell_tool.run(f"pytest {test_file} --json-report --json-report-file={json_report_file} --cov={test_file.replace('_test.py', '.py')}")
        
        try:
            # Read the JSON report file
            with open(json_report_file, 'r') as f:
                report_data = json.load(f)
            
            # Clean up the report file
            os.remove(json_report_file)
            
            return report_data
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading test results: {str(e)}")
            return {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "error": str(e)
            }

    def analyze_failures(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze test failures and suggest fixes."""
        prompt = f"""Analyze these test results and provide detailed suggestions:
        {json.dumps(test_results, indent=2)}
        
        Please provide:
        1. Analysis of each failure
        2. Root cause identification
        3. Specific suggestions for fixes
        4. Best practices to prevent similar issues
        """
        
        response = self.llm.invoke(prompt)
        return {"analysis": response.content, "results": test_results}

    def generate_report(self, test_results: Dict[str, Any], failure_analysis: Dict[str, Any] = None) -> str:
        """Generate a human-readable test execution report."""
        context = ""
        if failure_analysis:
            context = f"""Based on the failure analysis:
            {failure_analysis['analysis']}
            """
        
        prompt = f"""{context}
        Generate a detailed test execution report based on these results:
        {json.dumps(test_results, indent=2)}
        
        Include:
        1. Total number of tests
        2. Number of passed/failed tests
        3. Code coverage statistics
        4. Detailed analysis of failures
        5. Suggestions for fixing failed tests
        6. Recommendations for improving test quality
        7. Next steps and priorities
        """
        
        response = self.llm.invoke(prompt)
        return response.content

    def get_tools(self) -> List[Tool]:
        """Get all available tools with their descriptions."""
        return [
            Tool(
                name="scan_directory",
                func=self.scan_directory,
                description="""Scan a directory for source code files. 
                Input: directory path to scan
                Output: list of Python and JSON files found
                Use this to discover source files that need testing."""
            ),
            Tool(
                name="analyze_code",
                func=self.analyze_code,
                description="""Analyze source code to understand its structure and functionality.
                Input: path to source file
                Output: analysis of code structure, dependencies, and key functionality
                Use this to understand what needs to be tested."""
            ),
            Tool(
                name="generate_test",
                func=self.generate_test,
                description="""Generate test cases for a source code file.
                Input: path to source file and optional analysis results
                Output: generated test code
                Use this to create comprehensive test cases."""
            ),
            Tool(
                name="execute_test",
                func=self.execute_test,
                description="""Execute test cases using pytest.
                Input: path to test file
                Output: test execution results including coverage
                Use this to run tests and gather results."""
            ),
            Tool(
                name="analyze_failures",
                func=self.analyze_failures,
                description="""Analyze test failures and suggest fixes.
                Input: test execution results
                Output: analysis of failures and suggested fixes
                Use this to understand and fix test failures."""
            ),
            Tool(
                name="generate_report",
                func=self.generate_report,
                description="""Generate a test execution report.
                Input: test results and analysis
                Output: comprehensive test report
                Use this to create detailed reports."""
            ),
            Tool(
                name=self.shell_tool.name,  # Assuming your shell_tool has a name attribute
                func=self.shell_tool.run,   # Assuming your shell_tool has a run method
                description=self.shell_tool.description, # Assuming it has a description
            )
        ] 