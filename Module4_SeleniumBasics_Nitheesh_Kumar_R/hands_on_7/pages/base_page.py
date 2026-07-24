from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """Base class for all Page Objects. Contains common methods for interacting with the browser."""
    def __init__(self, driver):
        self.driver = driver

    def navigate_to(self, url):
        """Navigate to the specified URL."""
        self.driver.get(url)

    def get_title(self):
        """Get the current page title."""
        return self.driver.title

    def wait_for_element(self, locator, timeout=10):
        """Wait for an element to be present in the DOM and return it."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
    
    def wait_for_element_visible(self, locator, timeout=10):
        """Wait for an element to be visible in the DOM and return it."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_element_clickable(self, locator, timeout=10):
        """Wait for an element to be clickable and return it."""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def click(self, locator, timeout=10):
        """Wait for an element to be clickable, then click it."""
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()

    def type_text(self, locator, text, timeout=10):
        """Wait for an element to be visible, clear it, and type text."""
        element = self.wait_for_element_visible(locator, timeout)
        element.clear()
        element.send_keys(text)
        
    def get_text(self, locator, timeout=10):
        """Wait for an element to be visible and return its text."""
        element = self.wait_for_element_visible(locator, timeout)
        return element.text
