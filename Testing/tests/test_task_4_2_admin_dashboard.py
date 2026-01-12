"""
Test cases for Task 4 - Subtask 4.2: Admin Dashboard UI
Tests using Playwright with JSON test case definitions
"""

import pytest
import json
from pathlib import Path
from playwright.sync_api import Page, expect


# Load JSON test cases
TEST_CASES_FILE = Path(__file__).parent / "test_cases" / "task_4_2_admin_dashboard.json"

with open(TEST_CASES_FILE) as f:
    TEST_CONFIG = json.load(f)


@pytest.mark.e2e
class TestTask42AdminDashboard:
    """End-to-end tests for Admin Dashboard UI wireframe"""
    
    @pytest.fixture(autouse=True)
    def load_test_cases(self):
        """Load test cases from JSON"""
        self.test_cases = TEST_CONFIG["test_cases"]
    
    def _run_assertions(self, page: Page, assertions):
        """Helper method to run assertions"""
        for assertion in assertions:
            if assertion["type"] == "title_contains":
                expect(page).to_have_title(lambda title: assertion["value"].lower() in title.lower())
            elif assertion["type"] == "element_visible":
                locator = page.locator(assertion["selector"])
                expect(locator).to_be_visible()
                if "text" in assertion:
                    expect(locator).to_contain_text(assertion["text"])
            elif assertion["type"] == "element_count":
                count = page.locator(assertion["selector"]).count()
                if "min_count" in assertion:
                    assert count >= assertion["min_count"], f"Expected at least {assertion['min_count']} elements, got {count}"
                else:
                    assert count == assertion["count"], f"Expected {assertion['count']} elements, got {count}"
            elif assertion["type"] == "element_contains_text":
                locator = page.locator(assertion["selector"])
                expect(locator.first).to_contain_text(assertion["text"])
    
    def test_admin_dashboard_loads(self, page: Page, live_server):
        """Test admin dashboard loads and displays correctly"""
        test_case = next(tc for tc in self.test_cases if tc["name"] == "admin_dashboard_loads")
        # Note: This test requires authentication - would need login setup in actual implementation
        page.goto(f"{live_server.url}{test_case['url']}")
        self._run_assertions(page, test_case["assertions"])
    
    def test_admin_dashboard_stat_cards(self, page: Page, live_server):
        """Test admin dashboard displays stat cards"""
        test_case = next(tc for tc in self.test_cases if tc["name"] == "admin_dashboard_stat_cards")
        page.goto(f"{live_server.url}{test_case['url']}")
        self._run_assertions(page, test_case["assertions"])
    
    def test_admin_dashboard_quick_actions(self, page: Page, live_server):
        """Test admin dashboard has quick action links"""
        test_case = next(tc for tc in self.test_cases if tc["name"] == "admin_dashboard_quick_actions")
        page.goto(f"{live_server.url}{test_case['url']}")
        self._run_assertions(page, test_case["assertions"])

