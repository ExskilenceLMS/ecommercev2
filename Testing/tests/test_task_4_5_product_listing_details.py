"""
Test cases for Task 4 - Subtask 4.5: Product Listing & Details UI
Tests using Playwright with JSON test case definitions
"""

import pytest
import json
from pathlib import Path
from playwright.sync_api import Page, expect


# Load JSON test cases
TEST_CASES_FILE = Path(__file__).parent / "test_cases" / "task_4_5_product_listing_details.json"

with open(TEST_CASES_FILE) as f:
    TEST_CONFIG = json.load(f)


@pytest.mark.e2e
class TestTask45ProductListingDetails:
    """End-to-end tests for Product Listing & Details UI wireframes"""
    
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
    
    def test_product_listing_page_loads(self, page: Page, live_server):
        """Test product listing page loads and displays correctly"""
        test_case = next(tc for tc in self.test_cases if tc["name"] == "product_listing_page_loads")
        page.goto(f"{live_server.url}{test_case['url']}")
        self._run_assertions(page, test_case["assertions"])
    
    def test_product_listing_search_filter(self, page: Page, live_server):
        """Test product listing has search and filter controls"""
        test_case = next(tc for tc in self.test_cases if tc["name"] == "product_listing_search_filter")
        page.goto(f"{live_server.url}{test_case['url']}")
        self._run_assertions(page, test_case["assertions"])
    
    def test_product_listing_grid(self, page: Page, live_server):
        """Test product listing displays products in grid"""
        test_case = next(tc for tc in self.test_cases if tc["name"] == "product_listing_grid")
        page.goto(f"{live_server.url}{test_case['url']}")
        self._run_assertions(page, test_case["assertions"])
    
    def test_product_details_page_structure(self, page: Page, live_server):
        """Test product details page has correct structure"""
        test_case = next(tc for tc in self.test_cases if tc["name"] == "product_details_page_structure")
        page.goto(f"{live_server.url}{test_case['url']}")
        self._run_assertions(page, test_case["assertions"])
    
    def test_product_details_add_to_cart(self, page: Page, live_server):
        """Test product details page has add to cart form"""
        test_case = next(tc for tc in self.test_cases if tc["name"] == "product_details_add_to_cart")
        page.goto(f"{live_server.url}{test_case['url']}")
        self._run_assertions(page, test_case["assertions"])

