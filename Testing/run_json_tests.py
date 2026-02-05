#!/usr/bin/env python3
"""
Generic Test Runner for JSON Test Case Files
Runs static and dynamic validation tests from any JSON test case file
"""

import json
import sys
import subprocess
import os
import re
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DEVELOPMENT_DIR = PROJECT_ROOT / "Development"
TEST_CASES_DIR = Path(__file__).parent / "tests" / "test_cases"
TESTS_DIR = Path(__file__).parent / "tests"


def load_test_config(json_file_path):
    """Load test configuration from JSON file"""
    json_path = Path(json_file_path)
    
    # If relative path, try to resolve it
    if not json_path.is_absolute():
        # Try as-is first
        if not json_path.exists():
            # Try in test_cases directory
            json_path = TEST_CASES_DIR / json_path.name
        if not json_path.exists():
            # Try with full path from test_cases
            json_path = TEST_CASES_DIR / json_path
    
    if not json_path.exists():
        raise FileNotFoundError(f"Test cases file not found: {json_file_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f), json_path


def run_static_validation(config):
    """Run static HTML and CSS validation"""
    validation = config.get("validation", {})
    static = validation.get("static", {})
    
    if not static.get("required", False):
        print("\n⚠️  Static validation not required")
        return True
    
    print("\n" + "="*60)
    print("STATIC VALIDATION")
    print("="*60)
    
    results = {"html": True, "css": True, "js": True}
    
    # HTML Validation
    html_config = static.get("html", {})
    if html_config.get("isMandatory", False):
        print("\n📄 HTML Validation:")
        html_rules = html_config.get("rules", [])
        
        if not html_rules:
            print("  ⚠️  No HTML rules defined")
        else:
            for rule in html_rules:
                file_path = DEVELOPMENT_DIR / rule["file"]
                required_elements = rule.get("requiredElements", [])
                
                print(f"  Checking: {rule['file']}")
                
                if not file_path.exists():
                    print(f"    ❌ File not found: {file_path}")
                    results["html"] = False
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    missing = []
                    for element in required_elements:
                        # Simple regex check for HTML elements
                        # Look for <element or </element
                        pattern = rf'<{element}[>\s]|</{element}>'
                        if not re.search(pattern, content, re.IGNORECASE):
                            missing.append(element)
                    
                    if missing:
                        print(f"    ❌ Missing elements: {', '.join(missing)}")
                        results["html"] = False
                    else:
                        print(f"    ✅ All required elements found: {', '.join(required_elements)}")
                except Exception as e:
                    print(f"    ❌ Error parsing HTML: {e}")
                    results["html"] = False
    
    # CSS Validation
    css_config = static.get("css", {})
    if css_config.get("isMandatory", False):
        print("\n🎨 CSS Validation:")
        css_rules = css_config.get("rules", [])
        
        if not css_rules:
            print("  ⚠️  No CSS rules defined")
        else:
            for rule in css_rules:
                file_path = DEVELOPMENT_DIR / rule["file"]
                required_selectors = rule.get("requiredSelectors", [])
                
                print(f"  Checking: {rule['file']}")
                
                if not file_path.exists():
                    print(f"    ❌ File not found: {file_path}")
                    results["css"] = False
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    missing = []
                    for selector in required_selectors:
                        # Look for CSS selector - can be .selector, .selector {, .selector:, etc.
                        # Remove leading . or # for matching
                        clean_selector = selector.lstrip('.#')
                        # Check for various patterns: .selector, .selector {, .selector:, .selector\n, etc.
                        patterns = [
                            f".{clean_selector}",
                            f"#{clean_selector}",
                            selector,
                        ]
                        found = False
                        for pattern in patterns:
                            # Check if pattern appears as a CSS selector (followed by {, :, space, or newline)
                            if re.search(rf'{re.escape(pattern)}\s*[{{:\s\n]', content):
                                found = True
                                break
                        if not found:
                            missing.append(selector)
                    
                    if missing:
                        print(f"    ❌ Missing selectors: {', '.join(missing)}")
                        results["css"] = False
                    else:
                        print(f"    ✅ All required selectors found: {', '.join(required_selectors)}")
                except Exception as e:
                    print(f"    ❌ Error parsing CSS: {e}")
                    results["css"] = False
    
    # JavaScript Validation (if needed in future)
    js_config = static.get("js", {})
    if js_config.get("isMandatory", False):
        print("\n📜 JavaScript Validation:")
        js_rules = js_config.get("rules", [])
        
        if not js_rules:
            print("  ⚠️  No JavaScript rules defined")
        else:
            for rule in js_rules:
                file_path = DEVELOPMENT_DIR / rule["file"]
                required_functions = rule.get("requiredFunctions", [])
                
                print(f"  Checking: {rule['file']}")
                
                if not file_path.exists():
                    print(f"    ❌ File not found: {file_path}")
                    results["js"] = False
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    missing = []
                    for func in required_functions:
                        # Look for function definitions
                        pattern = rf'function\s+{re.escape(func)}|const\s+{re.escape(func)}\s*=|let\s+{re.escape(func)}\s*=|var\s+{re.escape(func)}\s*='
                        if not re.search(pattern, content):
                            missing.append(func)
                    
                    if missing:
                        print(f"    ❌ Missing functions: {', '.join(missing)}")
                        results["js"] = False
                    else:
                        print(f"    ✅ All required functions found: {', '.join(required_functions)}")
                except Exception as e:
                    print(f"    ❌ Error parsing JavaScript: {e}")
                    results["js"] = False
    
    # Return True only if all required validations passed
    return all(results.values())


def find_test_file(json_file_path):
    """Find corresponding pytest test file for a JSON test case file"""
    json_name = Path(json_file_path).stem  # Get filename without extension
    
    # Try different naming patterns
    possible_names = [
        json_name,  # Exact match
        json_name.replace("_", "-"),  # With dashes
        f"test_{json_name}",  # With test_ prefix
        json_name.replace("task_", "test_task_"),  # task_ -> test_task_
    ]
    
    for name in possible_names:
        # Try .py extension
        test_file = TESTS_DIR / f"{name}.py"
        if test_file.exists():
            return test_file
    
    return None


def run_dynamic_validation(config, json_file_path):
    """Run dynamic Playwright tests"""
    validation = config.get("validation", {})
    dynamic = validation.get("dynamic", {})
    
    if not dynamic.get("required", False):
        print("\n⚠️  Dynamic tests not required")
        return True
    
    print("\n" + "="*60)
    print("DYNAMIC VALIDATION (Playwright Tests)")
    print("="*60)
    
    # Check if Flask app exists
    flask_config = dynamic.get("flaskConfig", {})
    app_path_str = flask_config.get("appPath", "Development/app.py")
    app_path = PROJECT_ROOT / app_path_str
    
    if not app_path.exists() or app_path.read_text().strip() == "":
        print("\n⚠️  Flask app not found or empty. Skipping dynamic tests.")
        print(f"   Expected app at: {app_path}")
        print("   Please set up the Flask application first.")
        return False
    
    # Find corresponding test file
    test_file = find_test_file(json_file_path)
    
    if not test_file:
        print(f"\n⚠️  No corresponding pytest test file found for: {Path(json_file_path).name}")
        print(f"   Searched in: {TESTS_DIR}")
        print("   Dynamic tests require a pytest test file.")
        return False
    
    print(f"\n🧪 Running Playwright tests: {test_file.name}")
    
    # Set PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = str(DEVELOPMENT_DIR)
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_file), "-v", "--tb=short"],
            cwd=PROJECT_ROOT,
            env=env,
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def run_pytest_validation(config):
    """Run pytest unit tests if specified"""
    validation = config.get("validation", {})
    pytest_config = validation.get("pytest", {})
    
    if not pytest_config.get("required", False):
        return True
    
    print("\n" + "="*60)
    print("PYTEST VALIDATION")
    print("="*60)
    
    # This would run pytest tests if specified in the config
    # For now, we'll rely on the dynamic validation to run pytest tests
    print("⚠️  Pytest validation handled by dynamic validation")
    return True


def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(
        description="Run tests from JSON test case files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_json_tests.py task_4_1_login_registration.json
  python run_json_tests.py tests/test_cases/task_4_1_login_registration.json
  python run_json_tests.py --list  # List all available JSON test files
        """
    )
    
    parser.add_argument(
        "json_file",
        nargs="?",
        help="Path to JSON test case file (relative or absolute)"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available JSON test case files"
    )
    
    args = parser.parse_args()
    
    # List available test files
    if args.list:
        print("\n📚 Available JSON Test Case Files:\n")
        if TEST_CASES_DIR.exists():
            json_files = sorted(TEST_CASES_DIR.glob("*.json"))
            if json_files:
                for json_file in json_files:
                    print(f"  • {json_file.name}")
            else:
                print("  No JSON test case files found")
        else:
            print(f"  Test cases directory not found: {TEST_CASES_DIR}")
        return
    
    # Require JSON file argument
    if not args.json_file:
        parser.print_help()
        sys.exit(1)
    
    # Get task name from JSON file
    try:
        config, json_path = load_test_config(args.json_file)
        task_id = config.get("id", Path(json_path).stem)
        task_name = config.get("name", task_id)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        sys.exit(1)
    
    print(f"🧪 Running Tests: {task_name}")
    print(f"📄 Test File: {json_path.name}")
    print("="*60)
    
    # Run validations
    static_passed = run_static_validation(config)
    dynamic_passed = run_dynamic_validation(config, json_path)
    pytest_passed = run_pytest_validation(config)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Static Validation:  {'✅ PASSED' if static_passed else '❌ FAILED'}")
    print(f"Dynamic Validation: {'✅ PASSED' if dynamic_passed else '❌ FAILED'}")
    print(f"Pytest Validation:  {'✅ PASSED' if pytest_passed else '❌ FAILED'}")
    
    all_passed = static_passed and dynamic_passed and pytest_passed
    
    if all_passed:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
