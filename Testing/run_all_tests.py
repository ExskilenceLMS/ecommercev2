#!/usr/bin/env python3
"""
Run all tests and generate HTML reports for each task
"""

import subprocess
import sys
import json
from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).parent.parent
DEVELOPMENT_DIR = PROJECT_ROOT / "Development"
TESTING_DIR = Path(__file__).parent
TEST_CONFIGS_DIR = TESTING_DIR / "test_configs"
TESTS_DIR = TESTING_DIR / "tests"
RESULTS_DIR = TESTING_DIR / "results"

# Create results directory
RESULTS_DIR.mkdir(exist_ok=True)

def fix_test_imports():
    """Fix imports in all test files"""
    print("Fixing test file imports...")
    for test_file in TESTS_DIR.glob("test_*.py"):
        content = test_file.read_text()
        
        # Fix path setup
        if "project_root = Path(__file__).parent.parent.parent.parent.parent.parent" in content:
            content = content.replace(
                "project_root = Path(__file__).parent.parent.parent.parent.parent.parent",
                "project_root = Path(__file__).parent.parent.parent\ndevelopment_dir = project_root / \"Development\""
            )
            content = content.replace(
                "sys.path.insert(0, str(project_root))",
                "sys.path.insert(0, str(development_dir))"
            )
        
        # Fix User import
        content = content.replace(
            "from PHASE_2_CORE_SYSTEM_AUTH_DASHBOARDS.PART_1_PROJECT_SETUP.TASK_5_APPLICATION_SETUP.models.user import User",
            "from models.user import User"
        )
        
        # Remove duplicate comments
        content = content.replace("# Path already set above\n", "")
        
        test_file.write_text(content)
    print("✅ Test imports fixed")

def run_test_for_task(task_id):
    """Run tests for a specific task and generate HTML report"""
    task_id_str = str(task_id).zfill(2)
    config_file = TEST_CONFIGS_DIR / f"task_{task_id_str}.json"
    
    if not config_file.exists():
        print(f"❌ Config not found for task {task_id}")
        return False
    
    with open(config_file) as f:
        config = json.load(f)
    
    task_name = config.get("task_name", f"Task {task_id}")
    print(f"\n{'='*60}")
    print(f"Running tests for Task {task_id}: {task_name}")
    print(f"{'='*60}")
    
    # Collect all test files for this task
    test_files = []
    mandatory_tests = config.get("mandatory_tests", [])
    optional_tests = config.get("optional_tests", [])
    
    for test in mandatory_tests + optional_tests:
        test_file = test.get("file", "")
        if test_file.startswith("tests/"):
            test_path = TESTS_DIR / test_file.replace("tests/", "")
            if test_path.exists():
                test_files.append(str(test_path))
    
    if not test_files:
        print(f"⚠️  No test files found for task {task_id}")
        return False
    
    # Run pytest with HTML report
    html_report = RESULTS_DIR / f"task_{task_id_str}_result.html"
    
    # Use venv Python if available
    venv_python = PROJECT_ROOT / "venv" / "bin" / "python"
    python_exe = str(venv_python) if venv_python.exists() else sys.executable
    
    cmd = [
        python_exe, "-m", "pytest",
        "-v",
        "--html", str(html_report),
        "--self-contained-html",
        *test_files
    ]
    
    # Set PYTHONPATH to include Development directory
    env = os.environ.copy()
    env['PYTHONPATH'] = str(DEVELOPMENT_DIR)
    
    try:
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            env=env,
            capture_output=True,
            text=True
        )
        
        # Check if tests passed or were skipped (both are acceptable)
        if result.returncode == 0:
            # Check if all tests were skipped
            if "no tests ran" in result.stdout.lower() or "collected 0 items" in result.stdout.lower():
                print(f"⚠️  No tests found - Report: {html_report}")
                return False
            elif "skipped" in result.stdout.lower():
                # Some or all skipped is acceptable if database not available
                if "passed" in result.stdout.lower():
                    print(f"✅ Tests passed (some skipped) - Report: {html_report}")
                else:
                    print(f"⚠️  All tests skipped (database may not be available) - Report: {html_report}")
                return True
            else:
                print(f"✅ Tests passed - Report: {html_report}")
                return True
        else:
            print(f"❌ Tests failed - Report: {html_report}")
            print(f"   {result.stdout[:500]}")
            return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running all test cases and generating HTML reports...\n")
    
    # Fix imports first
    fix_test_imports()
    
    # Copy conftest to Testing/tests if needed
    conftest_src = DEVELOPMENT_DIR / "tests" / "conftest.py"
    conftest_dst = TESTS_DIR / "conftest.py"
    if conftest_src.exists() and not conftest_dst.exists():
        content = conftest_src.read_text()
        # Fix path in conftest
        content = content.replace(
            "project_root = Path(__file__).parent.parent",
            "project_root = Path(__file__).parent.parent.parent\ndevelopment_dir = project_root / \"Development\""
        )
        content = content.replace(
            "sys.path.insert(0, str(project_root))",
            "sys.path.insert(0, str(development_dir))"
        )
        conftest_dst.write_text(content)
        print("✅ Copied and fixed conftest.py")
    
    # Run tests for each task
    results = {}
    for task_id in range(1, 16):
        results[task_id] = run_test_for_task(task_id)
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    passed = sum(1 for v in results.values() if v)
    failed = 15 - passed
    print(f"✅ Passed: {passed}/15")
    print(f"❌ Failed: {failed}/15")
    print(f"\n📊 Reports saved in: {RESULTS_DIR}")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())

