"""
Test cases for Task 4 - Subtask 4.1: Login & Registration UI
Tests using Playwright with JSON test case definitions
"""

import pytest
import json
import sys
from pathlib import Path
from playwright.sync_api import Page, expect

# Add Development directory to path
project_root = Path(__file__).parent.parent.parent
development_dir = project_root / "Development"
sys.path.insert(0, str(development_dir))

# Load JSON test cases
TEST_CASES_FILE = Path(__file__).parent / "test_cases" / "task_4_1_login_registration.json"

with open(TEST_CASES_FILE) as f:
    TEST_CONFIG = json.load(f)

# Get test cases from validation.dynamic.tests
TEST_CASES = TEST_CONFIG.get("validation", {}).get("dynamic", {}).get("tests", [])
BASE_URL = TEST_CONFIG.get("validation", {}).get("dynamic", {}).get("baseUrl", "http://localhost:5000")




@pytest.mark.e2e
class TestTask41LoginRegistration:
    """End-to-end tests for Login & Registration UI wireframes"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test cases"""
        self.test_cases = TEST_CASES
        self.base_url = BASE_URL
    
    def _run_test_case(self, page: Page, test_case_name: str, live_server):
        """Helper method to run a test case from JSON"""
        test_case = next(
            (tc for tc in self.test_cases if tc["name"] == test_case_name),
            None
        )
        
        if not test_case:
            pytest.skip(f"Test case '{test_case_name}' not found in JSON")
        
        # Navigate to the page
        url = f"{live_server.url}{test_case['path']}"
        page.goto(url, wait_until="networkidle")
        
        # Capture screenshot if requested
        if test_case.get("captureScreenshot"):
            screenshot_path = Path(__file__).parent.parent / "results" / f"{test_case_name.replace(' ', '_')}.png"
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshot_path))
        
        # Run assertions
        for assertion in test_case.get("assertions", []):
            selector = assertion.get("selector")
            assertion_type = assertion.get("type")
            
            if assertion_type == "visible":
                locator = page.locator(selector)
                expect(locator).to_be_visible(timeout=5000)
            elif assertion_type == "exists":
                locator = page.locator(selector)
                expect(locator).to_have_count(1, timeout=5000)
            elif assertion_type == "count":
                locator = page.locator(selector)
                expected_count = assertion.get("count", 1)
                expect(locator).to_have_count(expected_count, timeout=5000)
    
    def test_login_page_loads_correctly(self, page: Page, live_server):
        """Test login page loads and displays correctly"""
        self._run_test_case(page, "Login page loads correctly", live_server)
    
    def test_register_page_loads_correctly(self, page: Page, live_server):
        """Test registration page loads and displays correctly"""
        self._run_test_case(page, "Register page loads correctly", live_server)
    
    def test_login_form_structure(self, page: Page, live_server):
        """Test login form has correct structure"""
        self._run_test_case(page, "Login form structure", live_server)
    
    def test_register_form_structure(self, page: Page, live_server):
        """Test registration form has correct structure"""
        self._run_test_case(page, "Register form structure", live_server)

