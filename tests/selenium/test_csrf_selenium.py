"""
Headless Selenium smoke test for CSRF-protected flows.

Requirements (install locally):
  pip install selenium webdriver-manager

Run locally (not executed here):
  python -m pytest tests/selenium/test_csrf_selenium.py

This script opens the homepage, fills login form, submits and checks for navigation.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


def test_login_flow():
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    try:
        driver.get('https://aaditech2.pythonanywhere.com/accounts/login/')
        time.sleep(1)
        # Fill identifier and password
        ident = driver.find_element(By.ID, 'identifier')
        pwd = driver.find_element(By.ID, 'password')
        ident.send_keys('testuser')
        pwd.send_keys('pass1234')

        # Submit
        submit = driver.find_element(By.CSS_SELECTOR, 'button[type=submit]')
        submit.click()
        time.sleep(2)

        # Basic check: URL changed or dashboard heading visible
        assert 'dashboard' in driver.current_url or 'Dashboard' in driver.page_source
    finally:
        driver.quit()
