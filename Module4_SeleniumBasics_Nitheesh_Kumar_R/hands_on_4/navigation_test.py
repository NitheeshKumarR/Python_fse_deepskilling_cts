from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import os

def main():
    # We will NOT run in headless for this task so screenshots render properly as requested (or we can run headless, 
    # but let's just use regular headless with a fixed window size for reliability in automated testing).
    options = Options()
    options.add_argument('--headless')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    """
    WINDOW SIZING:
    Demonstrating get_window_size() and set_window_size().
    Why consistent window size matters: In responsive web design, the UI changes based on screen resolution 
    (e.g., hamburger menus appear on small screens, elements wrap or disappear). By hardcoding a specific 
    window size, we ensure our automation interacts with the exact same UI layout across all machines and CI servers.
    """
    initial_size = driver.get_window_size()
    print(f"Initial Window Size: {initial_size}")
    
    driver.set_window_size(1280, 800)
    print(f"New Window Size: {driver.get_window_size()}")

    try:
        # Navigate to playground
        driver.get("https://www.lambdatest.com/selenium-playground/")
        print("\nNavigated to Playground.")

        # Navigate to the Simple Form Demo page by finding the link and clicking it
        # The link text is 'Simple Form Demo'
        link = driver.find_element(By.LINK_TEXT, "Simple Form Demo")
        link.click()
        
        # Give it a second to load
        time.sleep(1)

        # Assert the URL contains 'simple-form-demo'
        current_url = driver.current_url
        print(f"Current URL after click: {current_url}")
        assert 'simple-form-demo' in current_url, "Did not navigate to the Simple Form Demo page!"

        # Navigate back
        driver.back()
        print("Navigated back using driver.back()")

        # Open a new tab using execute_script
        print("\nOpening Google in a new tab...")
        driver.execute_script('window.open("https://www.google.com");')

        # List all open tabs and switch to the new one
        handles = driver.window_handles
        print(f"Open Window Handles: {handles}")
        
        driver.switch_to.window(handles[1])
        print(f"Switched to New Tab. Title: {driver.title}")

        # Switch back to the original tab
        driver.switch_to.window(handles[0])
        print(f"Switched back to Original Tab. Title: {driver.title}")

        # Take a screenshot
        screenshot_path = os.path.join(os.getcwd(), 'playground_screenshot.png')
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")

        # Verify the file is created
        assert os.path.exists(screenshot_path), "Screenshot file was not created!"
        print("Screenshot verification successful.")

    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    main()
