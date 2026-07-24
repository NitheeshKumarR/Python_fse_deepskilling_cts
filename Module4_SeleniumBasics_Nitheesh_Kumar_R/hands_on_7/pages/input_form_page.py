from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class InputFormPage(BasePage):
    """Page Object for the Input Form Submit page."""
    
    # Locators
    NAME_INPUT = (By.ID, 'name')
    EMAIL_INPUT = (By.ID, 'inputEmail4')
    PASSWORD_INPUT = (By.ID, 'inputPassword4')
    COMPANY_INPUT = (By.ID, 'company')
    WEBSITE_INPUT = (By.ID, 'websitename')
    CITY_INPUT = (By.ID, 'inputCity')
    ADDRESS_INPUT = (By.ID, 'inputAddress1')
    ADDRESS_2_INPUT = (By.ID, 'inputAddress2')
    STATE_INPUT = (By.ID, 'inputState')
    ZIP_INPUT = (By.ID, 'inputZip')
    
    # The submit button is typically a button type submit inside the form
    SUBMIT_BUTTON = (By.XPATH, "//button[text()='Submit']")
    
    # Success message div
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, '.success-msg')

    def fill_form(self, name, email, phone, address):
        """Fills out the essential form fields."""
        # Note: Depending on LambdaTest's form fields, phone might not exist, 
        # so we will map parameters to the closest fields (or use general fields).
        self.type_text(self.NAME_INPUT, name)
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, "Password123!") # Just filling a required field
        self.type_text(self.ADDRESS_INPUT, address)
        # Assuming we can just skip phone or it doesn't exist, if it does we'll just ignore for now or add it if needed.

    def submit_form(self):
        """Clicks the submit button."""
        self.click(self.SUBMIT_BUTTON)

    def get_success_message(self):
        """Returns the text of the success message after submission."""
        return self.get_text(self.SUCCESS_MESSAGE)
