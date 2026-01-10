#!/usr/bin/env python3
"""
Shared Test Runner for E-Commerce Project
Dynamically loads test configurations from JSON files and runs tests
"""

import json
import sys
import os
import subprocess
from pathlib import Path
import argparse

# Get the project root (parent of Testing directory)
PROJECT_ROOT = Path(__file__).parent.parent
DEVELOPMENT_DIR = PROJECT_ROOT / "Development"
TEST_CONFIGS_DIR = Path(__file__).parent / "test_configs"


def load_test_config(task_id):
    """Load test configuration for a given task ID"""
    task_id_str = str(task_id).zfill(2)  # Ensure 2-digit format
    config_file = TEST_CONFIGS_DIR / f"task_{task_id_str}.json"
    
    if not config_file.exists():
        print(f"❌ Test configuration not found: {config_file}")
        return None
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON config: {e}")
        return None
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return None


def run_test_file(test_file_path, task_name):
    """Run a test file using pytest"""
    # Convert relative path to absolute path
    # Test files are now in Testing/tests/
    if not os.path.isabs(test_file_path):
        test_file_path = Path(__file__).parent / test_file_path
    
    if not os.path.exists(test_file_path):
        print(f"   ⚠️  Test file not found: {test_file_path}")
        return False
    
    print(f"   🧪 Running: {test_file_path}")
    
    try:
        # Change to project root for pytest to work correctly
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_file_path), "-v"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"   ✅ Tests passed")
            return True
        else:
            print(f"   ❌ Tests failed")
            print(f"   {result.stdout}")
            if result.stderr:
                print(f"   {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ Error running tests: {e}")
        return False


def run_tests_for_task(task_id, run_optional=False):
    """Run tests for a specific task"""
    config = load_test_config(task_id)
    
    if not config:
        return False
    
    task_name = config.get("task_name", f"Task {task_id}")
    print(f"\n{'='*60}")
    print(f"📋 Task {task_id}: {task_name}")
    print(f"{'='*60}")
    print(f"Description: {config.get('description', 'N/A')}")
    
    all_passed = True
    
    # Run mandatory tests
    mandatory_tests = config.get("mandatory_tests", [])
    if mandatory_tests:
        print(f"\n🔴 Mandatory Tests ({len(mandatory_tests)}):")
        for test in mandatory_tests:
            test_file = test.get("file")
            test_name = test.get("name", "Unknown")
            print(f"\n   Test: {test_name}")
            if not run_test_file(test_file, task_name):
                all_passed = False
    else:
        print(f"\n⚠️  No mandatory tests defined")
    
    # Run optional tests if requested
    optional_tests = config.get("optional_tests", [])
    if optional_tests and run_optional:
        print(f"\n🟡 Optional Tests ({len(optional_tests)}):")
        for test in optional_tests:
            test_file = test.get("file")
            test_name = test.get("name", "Unknown")
            print(f"\n   Test: {test_name}")
            if not run_test_file(test_file, task_name):
                # Optional tests don't fail the overall run
                print(f"   ⚠️  Optional test failed (not blocking)")
    
    return all_passed


def list_all_tasks():
    """List all available tasks"""
    print("\n📚 Available Tasks:\n")
    for i in range(1, 16):
        config = load_test_config(i)
        if config:
            task_name = config.get("task_name", f"Task {i}")
            mandatory_count = len(config.get("mandatory_tests", []))
            optional_count = len(config.get("optional_tests", []))
            print(f"  Task {i:02d}: {task_name}")
            print(f"    Mandatory: {mandatory_count} | Optional: {optional_count}")
        else:
            print(f"  Task {i:02d}: Configuration not found")


def main():
    parser = argparse.ArgumentParser(
        description="E-Commerce Project Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python check_test.py 5              # Run tests for task 5
  python check_test.py 5 --optional   # Run mandatory + optional tests for task 5
  python check_test.py --all         # Run all tasks
  python check_test.py --list         # List all available tasks
        """
    )
    
    parser.add_argument(
        "task_id",
        nargs="?",
        type=int,
        help="Task ID (1-15) to run tests for"
    )
    
    parser.add_argument(
        "--optional",
        action="store_true",
        help="Also run optional tests"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run tests for all tasks"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available tasks"
    )
    
    args = parser.parse_args()
    
    # Validate project structure
    if not DEVELOPMENT_DIR.exists():
        print(f"❌ Development directory not found: {DEVELOPMENT_DIR}")
        print("   Please ensure the project structure is correct.")
        sys.exit(1)
    
    # Add Development to Python path for imports
    if DEVELOPMENT_DIR not in sys.path:
        sys.path.insert(0, str(DEVELOPMENT_DIR))
    
    if not TEST_CONFIGS_DIR.exists():
        print(f"❌ Test configs directory not found: {TEST_CONFIGS_DIR}")
        sys.exit(1)
    
    # Handle different modes
    if args.list:
        list_all_tasks()
        return
    
    if args.all:
        print("🚀 Running tests for all tasks...\n")
        all_passed = True
        for task_id in range(1, 16):
            if not run_tests_for_task(task_id, args.optional):
                all_passed = False
            print()  # Add spacing between tasks
        
        if all_passed:
            print("\n✅ All tasks passed!")
            sys.exit(0)
        else:
            print("\n❌ Some tasks failed!")
            sys.exit(1)
    
    if args.task_id:
        if args.task_id < 1 or args.task_id > 15:
            print(f"❌ Invalid task ID: {args.task_id}. Must be between 1 and 15.")
            sys.exit(1)
        
        success = run_tests_for_task(args.task_id, args.optional)
        if success:
            print("\n✅ Task completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Task failed!")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

