from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage

class DropdownPage(BasePage):
    """Page Object for the Dropdown Demo page."""
    
    # Locators
    DROPDOWN_SELECT = (By.ID, 'select-demo')

    def select_day(self, day_name):
        """Selects a day from the dropdown by its visible text."""
        element = self.wait_for_element(self.DROPDOWN_SELECT)
        select = Select(element)
        select.select_by_visible_text(day_name)
        
    def get_selected_day(self):
        """Returns the currently selected day."""
        element = self.wait_for_element(self.DROPDOWN_SELECT)
        select = Select(element)
        return select.first_selected_option.text
