from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time

def main():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # We DO NOT set implicitly_wait here, to demonstrate explicit waits!

    try:
        # Navigate to Bootstrap Alerts Demo
        driver.get("https://www.lambdatest.com/selenium-playground/bootstrap-alert-messages-demo")
        print("Navigated to Bootstrap Alerts Demo")

        # Find the "Normal Success Message" button (contains text "Normal Success Message")
        success_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Normal Success Message')]")
        
        """
        EXPLANATION: visibility_of_element_located vs element_to_be_clickable
        - visibility_of_element_located: Checks that the element is present in the DOM AND has a height/width > 0 (it is visible to the user).
        - element_to_be_clickable: Checks that the element is visible AND enabled AND not obscured by another element (e.g. a loading spinner overlay). 
          This is crucial for buttons, whereas visibility is sufficient for text elements like alerts.
        """
        
        # Wait until the button is clickable, then click it
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Normal Success Message')]")))
        
        # -------------------------------------------------------------
        # STEP 37: Demonstrate time.sleep() vs Explicit Wait
        # -------------------------------------------------------------
        
        # Test with time.sleep()
        print("\nTesting with time.sleep(3)...")
        start_time = time.time()
        success_btn.click()
        time.sleep(3) # Hard-coded sleep
        alert_divs = driver.find_elements(By.CSS_SELECTOR, '.alert-success')
        alert_div_sleep = next(div for div in alert_divs if div.is_displayed())
        print(f"Alert text is: '{alert_div_sleep.text}'")
        assert 'success' in alert_div_sleep.text.lower(), "Alert text mismatch"
        sleep_duration = time.time() - start_time
        print(f"time.sleep() took {sleep_duration:.2f} seconds.")
        
        # Refresh to clear the alert
        driver.refresh()
        success_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Normal Success Message')]")
        
        # Test with Explicit Wait
        print("\nTesting with Explicit Wait...")
        start_time_exp = time.time()
        success_btn.click()
        # Explicit wait polls the DOM and proceeds immediately when the condition is met, without waiting the full 10 seconds.
        # Use a custom lambda to find the visible one, or just find all and get the visible one
        alert_div_exp = WebDriverWait(driver, 10).until(
            lambda d: next((el for el in d.find_elements(By.CSS_SELECTOR, '.alert-success') if el.is_displayed()), None)
        )
        assert 'success' in alert_div_exp.text.lower(), "Alert text mismatch"
        exp_duration = time.time() - start_time_exp
        print(f"Explicit wait took {exp_duration:.2f} seconds.")
        print("Notice how explicit wait is much faster because it doesn't wait unnecessarily!")

        # -------------------------------------------------------------
        # STEP 39: FluentWait Demonstration
        # -------------------------------------------------------------
        print("\nDemonstrating Fluent Wait...")
        fluent_wait = WebDriverWait(driver, timeout=10, poll_frequency=0.5, ignored_exceptions=[NoSuchElementException])
        # Re-using the same alert just to demonstrate the fluent wait syntax
        success_btn.click()
        fluent_alert = fluent_wait.until(
            lambda d: next((el for el in d.find_elements(By.CSS_SELECTOR, '.alert-success') if el.is_displayed()), None)
        )
        print("Fluent wait successfully found the element by polling every 500ms and ignoring NoSuchElementException.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
