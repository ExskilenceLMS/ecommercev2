# Run Test Cases - Usage Guide

This guide explains how to use the generic test runner (`run_json_tests.py`) to execute test cases from JSON configuration files.

## Overview

The `run_json_tests.py` script is a generic test runner that can execute test cases from any JSON test case file. It supports:

- **Static Validation**: HTML, CSS, and JavaScript file validation
- **Dynamic Validation**: Playwright end-to-end tests
- **Pytest Validation**: Unit and integration tests

## Quick Start

### Basic Usage

```bash
# Run tests from a JSON test case file
python Testing/run_json_tests.py task_4_1_login_registration.json

# List all available JSON test case files
python Testing/run_json_tests.py --list

# Show help
python Testing/run_json_tests.py --help
```

## Command-Line Options

### Positional Arguments

- `json_file` (optional): Path to JSON test case file (relative or absolute)

### Optional Arguments

- `--list`: List all available JSON test case files in the `test_cases` directory
- `--help` or `-h`: Show help message and exit

## Usage Examples

### Example 1: Run Tests with Just Filename

If the JSON file is in the `Testing/tests/test_cases/` directory, you can use just the filename:

```bash
python Testing/run_json_tests.py task_4_1_login_registration.json
```

**Output:**
```
🧪 Running Tests: task4p1
📄 Test File: task_4_1_login_registration.json
============================================================

============================================================
STATIC VALIDATION
============================================================
...
```

### Example 2: Run Tests with Relative Path

You can also specify a relative path:

```bash
python Testing/run_json_tests.py tests/test_cases/task_4_1_login_registration.json
```

### Example 3: Run Tests with Absolute Path

For absolute paths:

```bash
python Testing/run_json_tests.py /full/path/to/task_4_1_login_registration.json
```

### Example 4: List Available Test Files

To see all available JSON test case files:

```bash
python Testing/run_json_tests.py --list
```

**Output:**
```
📚 Available JSON Test Case Files:

  • task_4_1_login_registration.json
  • task_5_2_product_management.json
  • task_6_1_checkout_process.json
```

## Test Execution Flow

The test runner executes tests in the following order:

1. **Static Validation**
   - HTML file validation (checks for required elements)
   - CSS file validation (checks for required selectors)
   - JavaScript file validation (checks for required functions)

2. **Dynamic Validation**
   - Checks if Flask app exists and is configured
   - Finds corresponding pytest test file
   - Runs Playwright end-to-end tests

3. **Pytest Validation**
   - Runs unit and integration tests (if specified)

4. **Summary Report**
   - Displays pass/fail status for each validation type
   - Provides overall test result

## Understanding Test Results

### Successful Test Run

```
============================================================
TEST SUMMARY
============================================================
Static Validation:  ✅ PASSED
Dynamic Validation: ✅ PASSED
Pytest Validation:  ✅ PASSED

✅ All tests passed!
```

### Failed Test Run

```
============================================================
TEST SUMMARY
============================================================
Static Validation:  ❌ FAILED
Dynamic Validation: ❌ FAILED
Pytest Validation:  ✅ PASSED

❌ Some tests failed!
```

### Common Issues and Solutions

#### Issue: Flask app not found

**Error:**
```
⚠️  Flask app not found or empty. Skipping dynamic tests.
   Expected app at: Development/app.py
```

**Solution:**
- Ensure `Development/app.py` exists and contains a Flask application
- The Flask app must be properly configured

#### Issue: Missing CSS selectors

**Error:**
```
❌ Missing selectors: .auth-box
```

**Solution:**
- Add the missing CSS selector to your stylesheet
- Or update the JSON test case file to match your implementation

#### Issue: Test file not found

**Error:**
```
⚠️  No corresponding pytest test file found for: task_4_1_login_registration.json
```

**Solution:**
- Create a corresponding pytest test file in `Testing/tests/`
- Naming convention: `test_<json_filename>.py` or match the JSON filename

## JSON Test Case File Structure

The test runner expects JSON files with the following structure:

```json
{
  "id": "task4p1",
  "name": "Task Name",
  "validation": {
    "static": {
      "required": true,
      "html": {
        "isMandatory": true,
        "rules": [
          {
            "file": "templates/auth/login.html",
            "requiredElements": ["form", "input", "button"]
          }
        ]
      },
      "css": {
        "isMandatory": true,
        "rules": [
          {
            "file": "static/css/style.css",
            "requiredSelectors": [".auth-container", ".btn-primary"]
          }
        ]
      }
    },
    "dynamic": {
      "required": true,
      "requiresFlask": true,
      "flaskConfig": {
        "appPath": "Development/app.py",
        "port": 5000,
        "startupTimeout": 15000
      },
      "baseUrl": "http://localhost:5000",
      "tests": [
        {
          "name": "Login page loads correctly",
          "path": "/auth/login",
          "assertions": [
            {"type": "visible", "selector": "form"}
          ]
        }
      ]
    },
    "pytest": {
      "required": true,
      "requiresFlask": false,
      "timeout": 30000
    }
  }
}
```

## Integration with CI/CD

You can integrate the test runner into your CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
- name: Run Test Cases
  run: |
    python Testing/run_json_tests.py task_4_1_login_registration.json
```

```bash
# Example shell script
#!/bin/bash
for json_file in Testing/tests/test_cases/*.json; do
    python Testing/run_json_tests.py "$json_file"
    if [ $? -ne 0 ]; then
        echo "Tests failed for $json_file"
        exit 1
    fi
done
```

## Environment Setup

### Prerequisites

- Python 3.7+
- Required packages (from `requirements.txt`):
  - `pytest>=7.0.0`
  - `pytest-playwright>=0.3.0`
  - `playwright>=1.30.0`
  - `pytest-flask>=1.2.0`

### Installing Playwright Browsers

If running dynamic tests, install Playwright browsers:

```bash
python -m playwright install chromium
```

## Tips and Best Practices

1. **Organize Test Files**: Keep JSON test case files in `Testing/tests/test_cases/` directory

2. **Naming Convention**: Use descriptive names like `task_4_1_login_registration.json`

3. **Test File Matching**: The runner automatically finds pytest test files matching the JSON filename

4. **Static vs Dynamic**: 
   - Static tests don't require a running Flask app
   - Dynamic tests require Flask app to be set up

5. **Debugging**: Use `-v` flag with pytest for verbose output (handled automatically)

## Troubleshooting

### Problem: Import errors when running tests

**Solution:** Ensure `PYTHONPATH` includes the `Development` directory. The test runner sets this automatically.

### Problem: Tests pass locally but fail in CI

**Solution:** 
- Check if Playwright browsers are installed in CI environment
- Verify Flask app can start in CI environment
- Check file paths are correct (use absolute paths if needed)

### Problem: CSS selector validation fails

**Solution:**
- Verify the selector exists in the CSS file
- Check for typos in selector names
- Ensure CSS file path in JSON is correct relative to `Development/` directory

## Additional Resources

- See `Testing/tests/test_cases/` for example JSON test case files
- Check `Testing/tests/` for corresponding pytest test files
- Review `pytest.ini` for pytest configuration

## Support

For issues or questions:
1. Check the error messages in the test output
2. Verify JSON file structure matches expected format
3. Ensure all required files exist in the correct locations
4. Review this documentation for common solutions
