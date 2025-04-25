import os
from playwright.sync_api import Page

def login(page: Page):
    """
    Shared login function for test cases
    
    Args:
        page: Playwright page object
    """
    print("Navigating to login page...")
    page.goto("http://localhost:8000/accounts/login/")
    
    # Wait for the page to load
    page.wait_for_load_state('networkidle')
    
    # Wait for and fill username
    username_input = page.wait_for_selector("#id_login", state="visible")
    username_input.fill(os.environ.get('admin_user'))
    
    # Wait for and fill password
    password_input = page.wait_for_selector("#id_password", state="visible")
    password_input.fill(os.environ.get('admin_password'))
    
    # Wait for and click submit button
    submit_button = page.wait_for_selector("button[type='submit']", state="visible")
    submit_button.click() 