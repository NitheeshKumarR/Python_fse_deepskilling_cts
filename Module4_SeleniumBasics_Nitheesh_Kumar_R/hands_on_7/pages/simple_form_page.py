from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class SimpleFormPage(BasePage):
    """Page Object for the Simple Form Demo page."""
    
    # Locators defined as class-level constants
    MESSAGE_INPUT = (By.ID, 'user-message')
    SUBMIT_BUTTON = (By.ID, 'showInput')
    DISPLAYED_MESSAGE = (By.ID, 'message')

    def enter_message(self, text):
        """Enters text into the message input field."""
        self.type_text(self.MESSAGE_INPUT, text)

    def click_submit(self):
        """Clicks the 'Get Checked Value' / submit button."""
        self.click(self.SUBMIT_BUTTON)

    def get_displayed_message(self):
        """Returns the text of the displayed message element."""
        return self.get_text(self.DISPLAYED_MESSAGE)
