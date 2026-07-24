import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

@pytest.fixture(scope='session')
def base_url():
    """Session-scoped fixture for the base URL."""
    return 'https://www.lambdatest.com/selenium-playground/'

@pytest.fixture(scope='function')
def driver(request):
    """Function-scoped fixture for WebDriver setup and teardown."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1280,800')
    
    # Initialize the driver
    web_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Make driver implicitly available in the request for the screenshot hook
    request.node.driver = web_driver
    
    # Yield hands control back to the test
    yield web_driver
    
    # Teardown happens after the test completes (or fails)
    web_driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture a screenshot if a test fails."""
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # we only look at actual failing test calls, not setup/teardown
    if rep.when == 'call' and rep.failed:
        # Check if the driver was successfully initialized and attached to the test node
        driver = getattr(item, 'driver', None)
        if driver:
            # Create a safe filename based on the test name
            test_name = item.name.replace('[', '_').replace(']', '_')
            screenshot_path = os.path.join(os.getcwd(), f"{test_name}_failure.png")
            try:
                driver.save_screenshot(screenshot_path)
                print(f"\nScreenshot saved to: {screenshot_path}")
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")
