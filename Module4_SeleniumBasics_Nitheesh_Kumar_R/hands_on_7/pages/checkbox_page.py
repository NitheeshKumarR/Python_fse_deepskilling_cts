from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckboxPage(BasePage):
    """Page Object for the Checkbox Demo page."""
    
    # Locators
    # To locate a specific checkbox by index, we can construct the locator dynamically or just grab the first one.
    # The exercise uses a specific single checkbox demo (isAgeSelected or similar).
    SINGLE_CHECKBOX = (By.CSS_SELECTOR, "input[type='checkbox']")

    def _get_checkbox(self):
        """Helper to get the checkbox element."""
        # This will grab the first checkbox on the page (matching our hands_on_6 implementation)
        return self.wait_for_element(self.SINGLE_CHECKBOX)

    def check_option(self):
        """Checks the checkbox if it is not already checked."""
        checkbox = self._get_checkbox()
        if not checkbox.is_selected():
            checkbox.click()

    def uncheck_option(self):
        """Unchecks the checkbox if it is currently checked."""
        checkbox = self._get_checkbox()
        if checkbox.is_selected():
            checkbox.click()

    def is_option_checked(self):
        """Returns True if the checkbox is checked, False otherwise."""
        return self._get_checkbox().is_selected()
