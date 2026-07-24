"""
SELENIUM ARCHITECTURE COMPONENTS:
1. WebDriver: The core component of Selenium that provides a programming interface to create and execute test cases. 
   It communicates directly with the browser using the browser's native automation API (like ChromeDriver for Chrome) 
   rather than relying on a Javascript sandbox.
2. Selenium Grid: A server that allows tests to use web browser instances running on remote machines. 
   It solves the problem of running tests across multiple machines and different browser/OS combinations in parallel, 
   drastically reducing test execution time.
3. Selenium IDE: A Chrome/Firefox extension that provides a record-and-playback tool for creating tests. 
   It is primarily used for quick prototyping, learning Selenium syntax, and generating boilerplate code, 
   but it is not suited for complex, maintainable automation frameworks.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def main():
    # Set up Chrome options for headless mode
    options = Options()
    options.add_argument('--headless')

    # Initialize WebDriver using webdriver_manager
    # webdriver_manager automatically downloads and manages the correct ChromeDriver version
    print("Setting up ChromeDriver...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    """
    IMPLICIT WAIT EXPLANATION:
    driver.implicitly_wait(10) tells WebDriver to poll the DOM for a certain amount of time when trying to find any element 
    if it is not immediately available.
    Why it is bad practice globally: It applies to ALL elements for the lifetime of the WebDriver instance. If an element 
    is legitimately missing, the script will painfully wait the full 10 seconds every single time before failing. It also 
    does not handle specific element states (like waiting for an element to be clickable, not just present), which explicit 
    waits handle much better.
    """
    driver.implicitly_wait(10)

    try:
        # Navigate to the Selenium Playground
        print("Navigating to LambdaTest Selenium Playground...")
        driver.get("https://www.lambdatest.com/selenium-playground/")

        # Print the page title
        print(f"Page Title: {driver.title}")

        # Verify title is printed correctly in headless mode
        assert "Selenium" in driver.title
        print("Success! Title verified in headless mode.")

    finally:
        # Close the browser instance entirely
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    main()
