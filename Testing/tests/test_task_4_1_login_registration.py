"""
Test cases for Task 4 - Subtask 4.1: Login & Registration UI
Tests using Playwright with JSON test case definitions
"""

import pytest
import json
from pathlib import Path
from playwright.sync_api import Page, expect


# Load JSON test cases
TEST_CASES_FILE = Path(__file__).parent / "test_cases" / "task_4_1_login_registration.json"

with open(TEST_CASES_FILE) as f:
    TEST_CONFIG = json.load(f)


@pytest.mark.e2e
class TestTask41LoginRegistration:
    """End-to-end tests for Login & Registration UI wireframes"""
    
    @pytest.fixture(autouse=True)
    def load_test_cases(self):
        """Load test cases from JSON"""
        self.test_cases = TEST_CONFIG["test_cases"]
    
    def test_login_page_loads(self, page: Page, live_server):
        """Test login page loads and displays correctly"""
        test_case = next(tc for tc in self.test_cases if tc["name"] == "login_page_loads")
        page.goto(f"{live_server.url}{test_case['url']}")
        
        for assertion in test_case["assertions"]:
            if assertion["type"] == "title_contains":
                expect(page).to_have_title(lambda title: assertion["value"].lower() in title.lower())
            elif assertion["type"] == "element_visible":
                locator = page.locator(assertion["selector"])
                expect(locator).to_be_visible()
                if "text" in assertion:
                    expect(locator).to_contain_text(assertion["text"])
            elif assertion["type"] == "element_count":
                count = page.locator(assertion["selector"]).count()
                assert count == assertion["count"], f"Expected {assertion['count']} elements, got {count}"
    
    def test_register_page_loads(self, page: Page, live_server):
        """Test registration page loads and displays correctly"""
        test_case = next(tc for tc in self.test_cases if tc["name"] == "register_page_loads")
        page.goto(f"{live_server.url}{test_case['url']}")
        
        for assertion in test_case["assertions"]:
            if assertion["type"] == "title_contains":
                expect(page).to_have_title(lambda title: assertion["value"].lower() in title.lower())
            elif assertion["type"] == "element_visible":
                locator = page.locator(assertion["selector"])
                expect(locator).to_be_visible()
                if "text" in assertion:
                    expect(locator).to_contain_text(assertion["text"])
    
    def test_login_form_structure(self, page: Page, live_server):
        """Test login form has correct structure"""
        test_case = next(tc for tc in self.test_cases if tc["name"] == "login_form_structure")
        page.goto(f"{live_server.url}{test_case['url']}")
        
        for assertion in test_case["assertions"]:
            if assertion["type"] == "element_count":
                count = page.locator(assertion["selector"]).count()
                assert count == assertion["count"], f"Expected {assertion['count']} elements, got {count}"
            elif assertion["type"] == "element_visible":
                expect(page.locator(assertion["selector"])).to_be_visible()
    
    def test_register_form_structure(self, page: Page, live_server):
        """Test registration form has correct structure"""
        test_case = next(tc for tc in self.test_cases if tc["name"] == "register_form_structure")
        page.goto(f"{live_server.url}{test_case['url']}")
        
        for assertion in test_case["assertions"]:
            if assertion["type"] == "element_count":
                count = page.locator(assertion["selector"]).count()
                assert count == assertion["count"], f"Expected {assertion['count']} elements, got {count}"
            elif assertion["type"] == "element_visible":
                expect(page.locator(assertion["selector"])).to_be_visible()

