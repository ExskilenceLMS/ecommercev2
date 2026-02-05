"""
Test cases for Task 4 - Subtask 4.2: Admin Dashboard UI
Tests using Playwright with JSON test case definitions
"""

import pytest
import json
import sys
import time
from pathlib import Path
from playwright.sync_api import Page, expect

# Add Development directory to path
project_root = Path(__file__).parent.parent.parent
development_dir = project_root / "Development"
sys.path.insert(0, str(development_dir))

# Load JSON test cases
TEST_CASES_FILE = Path(__file__).parent / "test_cases" / "task_4_2_admin_dashboard.json"

with open(TEST_CASES_FILE) as f:
    TEST_CONFIG = json.load(f)

# Get test cases from validation.dynamic.tests
TEST_CASES = TEST_CONFIG.get("validation", {}).get("dynamic", {}).get("tests", [])
BASE_URL = TEST_CONFIG.get("validation", {}).get("dynamic", {}).get("baseUrl", "http://localhost:5000")


@pytest.mark.e2e
class TestTask42AdminDashboard:
    """End-to-end tests for Admin Dashboard UI wireframe"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test cases"""
        self.test_cases = TEST_CASES
        self.base_url = BASE_URL
    
    def _run_actions(self, page: Page, actions, live_server):
        """Helper method to run actions from JSON"""
        for action in actions:
            action_type = action.get("type")
            
            if action_type == "fill":
                selector = action.get("selector")
                value = action.get("value")
                page.locator(selector).fill(value)
            elif action_type == "click":
                selector = action.get("selector")
                page.locator(selector).click()
            elif action_type == "wait":
                duration = action.get("duration", 1000)
                time.sleep(duration / 1000.0)  # Convert ms to seconds
            elif action_type == "goto":
                path = action.get("path")
                url = f"{live_server.url}{path}"
                page.goto(url, wait_until="networkidle")
    
    def _run_assertions(self, page: Page, assertions):
        """Helper method to run assertions from JSON"""
        for assertion in assertions:
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
                if "min" in assertion:
                    min_count = assertion.get("min", 1)
                    count = locator.count()
                    assert count >= min_count, f"Expected at least {min_count} elements, got {count}"
                elif "count" in assertion:
                    expected_count = assertion.get("count", 1)
                    expect(locator).to_have_count(expected_count, timeout=5000)
    
    def _run_test_case(self, page: Page, test_case_name: str, live_server):
        """Helper method to run a test case from JSON"""
        test_case = next(
            (tc for tc in self.test_cases if tc["name"] == test_case_name),
            None
        )
        
        if not test_case:
            pytest.skip(f"Test case '{test_case_name}' not found in JSON")
        
        # Run actions first (if any)
        actions = test_case.get("actions", [])
        if actions:
            self._run_actions(page, actions, live_server)
        else:
            # If no actions, navigate directly to the path
            url = f"{live_server.url}{test_case['path']}"
            page.goto(url, wait_until="networkidle")
        
        # Capture screenshot if requested
        if test_case.get("captureScreenshot"):
            screenshot_path = Path(__file__).parent.parent / "results" / f"{test_case_name.replace(' ', '_')}.png"
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshot_path))
        
        # Run assertions
        self._run_assertions(page, test_case.get("assertions", []))
    
    def test_admin_dashboard_loads_correctly(self, page: Page, live_server):
        """Test admin dashboard loads and displays correctly"""
        self._run_test_case(page, "Admin dashboard loads correctly", live_server)
    
    def test_admin_dashboard_displays_stat_cards(self, page: Page, live_server):
        """Test admin dashboard displays stat cards"""
        self._run_test_case(page, "Admin dashboard displays stat cards", live_server)
    
    def test_admin_dashboard_has_quick_action_links(self, page: Page, live_server):
        """Test admin dashboard has quick action links"""
        self._run_test_case(page, "Admin dashboard has quick action links", live_server)

