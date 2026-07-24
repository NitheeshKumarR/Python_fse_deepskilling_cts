import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Parameterize the form submission test with 3 different inputs
@pytest.mark.parametrize('message', ['Hello', 'Selenium Automation', '12345'])
def test_simple_form_submission(driver, base_url, message):
    driver.get(f"{base_url}simple-form-demo")
    
    # Locate the message input
    msg_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-message"))
    )
    
    # Enter the parameterized message
    msg_input.clear()
    msg_input.send_keys(message)
    
    # Click 'Get Checked Value' button (this acts as the Submit on this demo page)
    # The button text is typically "Get Checked Value"
    submit_btn = driver.find_element(By.ID, "showInput")
    submit_btn.click()
    
    # Wait for the message display element
    display_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )
    
    # Assert its text equals the parameterized message
    assert display_msg.text == message, f"Expected '{message}', got '{display_msg.text}'"

def test_checkbox_demo(driver, base_url):
    driver.get(f"{base_url}checkbox-demo")
    
    # Locate the first single checkbox
    checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='checkbox']"))
    )
    
    # Click it
    checkbox.click()
    
    # Assert it is selected
    assert checkbox.is_selected(), "Checkbox should be selected after first click"
    
    # Click it again
    checkbox.click()
    
    # Assert it is deselected
    assert not checkbox.is_selected(), "Checkbox should be deselected after second click"

def test_dropdown_selection(driver, base_url):
    driver.get(f"{base_url}select-dropdown-demo")
    
    # Locate the select element
    dropdown_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "select-demo"))
    )
    
    # Initialize the Select object
    dropdown = Select(dropdown_element)
    
    # Select 'Wednesday' by visible text
    dropdown.select_by_visible_text("Wednesday")
    
    # Assert the selected option text is 'Wednesday'
    selected_option = dropdown.first_selected_option
    assert selected_option.text == "Wednesday", f"Expected 'Wednesday', got '{selected_option.text}'"

def test_intentional_failure_for_screenshot(driver, base_url):
    """
    This test is designed to intentionally fail to demonstrate the screenshot on failure hook.
    You can remove or skip this later.
    """
    driver.get(base_url)
    # This assertion will fail, triggering the pytest_runtest_makereport hook in conftest.py
    assert "Invalid Title That Will Fail" in driver.title, "Intentional failure to trigger screenshot"
