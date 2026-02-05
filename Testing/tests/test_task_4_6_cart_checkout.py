"""
Test cases for Task 4 - Subtask 4.6: Cart & Checkout Flow UI
Tests using Playwright with JSON test case definitions
"""

import pytest
import json
from pathlib import Path
from playwright.sync_api import Page, expect


# Load JSON test cases
TEST_CASES_FILE = Path(__file__).parent / "test_cases" / "task_4_6_cart_checkout.json"

with open(TEST_CASES_FILE) as f:
    TEST_CONFIG = json.load(f)


@pytest.mark.e2e
class TestTask46CartCheckout:
    """End-to-end tests for Cart & Checkout Flow UI wireframes"""
    
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
    
    def test_cart_page_loads(self, page: Page, live_server):
        """Test cart page loads and displays correctly"""
        test_case = next(tc for tc in self.test_cases if tc["name"] == "cart_page_loads")
        page.goto(f"{live_server.url}{test_case['url']}")
        self._run_assertions(page, test_case["assertions"])
    
    def test_cart_table_structure(self, page: Page, live_server):
        """Test cart page has table structure for items"""
        test_case = next(tc for tc in self.test_cases if tc["name"] == "cart_table_structure")
        page.goto(f"{live_server.url}{test_case['url']}")
        self._run_assertions(page, test_case["assertions"])
    
    def test_cart_checkout_button(self, page: Page, live_server):
        """Test cart page has checkout button"""
        test_case = next(tc for tc in self.test_cases if tc["name"] == "cart_checkout_button")
        page.goto(f"{live_server.url}{test_case['url']}")
        self._run_assertions(page, test_case["assertions"])
    
    def test_checkout_review_page_loads(self, page: Page, live_server):
        """Test checkout review page loads and displays correctly"""
        test_case = next(tc for tc in self.test_cases if tc["name"] == "checkout_review_page_loads")
        page.goto(f"{live_server.url}{test_case['url']}")
        self._run_assertions(page, test_case["assertions"])
    
    def test_checkout_shipping_address(self, page: Page, live_server):
        """Test checkout page has shipping address section"""
        test_case = next(tc for tc in self.test_cases if tc["name"] == "checkout_shipping_address")
        page.goto(f"{live_server.url}{test_case['url']}")
        self._run_assertions(page, test_case["assertions"])
    
    def test_checkout_order_summary(self, page: Page, live_server):
        """Test checkout page has order summary section"""
        test_case = next(tc for tc in self.test_cases if tc["name"] == "checkout_order_summary")
        page.goto(f"{live_server.url}{test_case['url']}")
        self._run_assertions(page, test_case["assertions"])
    
    def test_checkout_place_order_button(self, page: Page, live_server):
        """Test checkout page has place order button"""
        test_case = next(tc for tc in self.test_cases if tc["name"] == "checkout_place_order_button")
        page.goto(f"{live_server.url}{test_case['url']}")
        self._run_assertions(page, test_case["assertions"])

