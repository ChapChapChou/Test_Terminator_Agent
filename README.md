# Automated Test Generator Agent

This project implements an LLM-powered agent that automatically generates, executes, and reports on test cases for Python and JSON files in a given directory.

## Features

- Recursively scans directories for Python and JSON source files
- Automatically generates comprehensive test cases with high code coverage
- Executes tests using pytest with coverage reporting
- Generates detailed test execution reports
- Provides suggestions for fixing failed tests

## Requirements

- Python 3.8+
- OpenAI API key

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Run the test generator agent:
```bash
python test_generator_agent.py
```

The agent will:
1. Scan the current directory for Python and JSON files
2. Generate test cases for each source file
3. Execute the tests
4. Generate a comprehensive report in `test_execution_report.txt`

## Test Generation

The agent generates test cases with the following features:
- 100% code coverage target
- Detailed comments explaining each test case
- Follows pytest conventions
- Test files are saved in the same directory as source files with '_test' suffix

## Test Execution

Tests are executed using pytest with:
- JSON report generation
- Code coverage reporting
- Detailed failure information

## Reports

The generated report includes:
- Total number of tests
- Number of passed/failed tests
- Code coverage statistics
- Detailed analysis of failures
- Suggestions for fixing failed tests 