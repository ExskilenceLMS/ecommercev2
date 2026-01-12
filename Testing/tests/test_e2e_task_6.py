"""
E2E tests for Task 6 using Playwright
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
@pytest.mark.auth
class TestTask6E2E:
    """End-to-end tests for Task 6: Login & Session Management"""
    
    def test_login_page_ui(self, page: Page, live_server):
        """Test login page UI elements"""
        page.goto(f"{live_server.url}/auth/login")
        
        expect(page).to_have_title("Login - E-Commerce")
        expect(page.locator("h2")).to_contain_text("Login")
        expect(page.locator('input[name="email"]')).to_be_visible()
        expect(page.locator('input[name="password"]')).to_be_visible()
        expect(page.locator('button[type="submit"]')).to_be_visible()
        expect(page.locator("text=Register")).to_be_visible()
    
    def test_register_page_ui(self, page: Page, live_server):
        """Test register page UI elements"""
        page.goto(f"{live_server.url}/auth/register")
        
        expect(page).to_have_title("Register - E-Commerce")
        expect(page.locator("h2")).to_contain_text("Register")
        expect(page.locator('input[name="email"]')).to_be_visible()
        expect(page.locator('input[name="password"]')).to_be_visible()
        expect(page.locator('input[name="confirm_password"]')).to_be_visible()
        expect(page.locator('input[name="first_name"]')).to_be_visible()
        expect(page.locator('input[name="last_name"]')).to_be_visible()
    
    def test_registration_flow(self, page: Page, live_server):
        """Test complete registration flow"""
        import random
        email = f"test{random.randint(1000, 9999)}@example.com"
        
        page.goto(f"{live_server.url}/auth/register")
        
        page.fill('input[name="email"]', email)
        page.fill('input[name="password"]', 'password123')
        page.fill('input[name="confirm_password"]', 'password123')
        page.fill('input[name="first_name"]', 'Test')
        page.fill('input[name="last_name"]', 'User')
        
        page.click('button[type="submit"]')
        
        # Should redirect to login or show success
        expect(page).to_have_url(f"{live_server.url}/auth/login", timeout=5000)
    
    def test_login_flow(self, page: Page, live_server):
        """Test login flow (requires existing user)"""
        # This test assumes a user exists
        # In real scenario, you'd create user first
        page.goto(f"{live_server.url}/auth/login")
        
        # Try to login with invalid credentials
        page.fill('input[name="email"]', 'nonexistent@example.com')
        page.fill('input[name="password"]', 'wrongpassword')
        page.click('button[type="submit"]')
        
        # Should show error or stay on login page
        expect(page.locator("text=Invalid") | page.locator("text=error")).to_be_visible(timeout=3000)
    
    def test_navigation_between_auth_pages(self, page: Page, live_server):
        """Test navigation between login and register"""
        page.goto(f"{live_server.url}/auth/login")
        page.click("text=Register")
        expect(page).to_have_url(f"{live_server.url}/auth/register")
        
        page.click("text=Login")
        expect(page).to_have_url(f"{live_server.url}/auth/login")

