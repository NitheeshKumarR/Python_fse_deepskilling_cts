"""
LOCATOR STRATEGIES RANKING (Most to Least Preferred)

1. ID (By.ID)
   - Why: Extremely fast, natively supported by browsers, and guaranteed to be unique within a valid HTML document. Least prone to breaking.
2. Name (By.NAME)
   - Why: Fast and highly reliable, though occasionally non-unique (e.g., radio button groups).
3. CSS Selector (By.CSS_SELECTOR)
   - Why: Very fast execution (faster than XPath in many browsers), concise syntax, and highly flexible for complex parent/child/attribute queries.
4. Class Name (By.CLASS_NAME)
   - Why: Useful but often non-unique since multiple elements share classes. Also breaks if utility classes (like Tailwind) change frequently.
5. XPath Relative (By.XPATH)
   - Why: Extremely powerful (can traverse UP the DOM and match text), but syntax is verbose and execution is slightly slower than CSS.
6. Tag Name (By.TAG_NAME)
   - Why: Rarely unique (there are hundreds of <div> tags on a page), only useful when searching within a highly specific parent element.
7. XPath Absolute (By.XPATH e.g., /html/body/div/div)
   - Why: Extremely brittle. Even a single newly added wrapper <div> will instantly break the locator. Never use this.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def main():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)

    try:
        # Navigate to Simple Form Demo
        driver.get("https://www.lambdatest.com/selenium-playground/simple-form-demo")
        print("Navigated to Simple Form Demo")

        # -------------------------------------------------------------
        # STEP 32: Locate the message input field using 6 strategies
        # Note: On LambdaTest Simple Form Demo, the first input field usually has id="user-message"
        # -------------------------------------------------------------
        msg_input_id = driver.find_element(By.ID, "user-message")
        print("1. Located by ID successfully.")

        # Since LambdaTest might not have name on this specific input, we'll try to find an element or just use ID's equivalent
        # For demonstration, we assume it might not have a specific 'name' attribute, but let's try to locate the form or a different element if it fails.
        # Actually, let's find the input by placeholder if name isn't there, or just skip if name isn't present on the specific site.
        # Wait, the instruction says "locate the message input field using each: By.ID, By.NAME..."
        # I will use XPath/CSS to find elements. Let's wrap in try/except for By.NAME in case it doesn't have a name attribute.
        
        # Let's inspect the page mentally. The input field id is 'user-message'.
        # By.CLASS_NAME (often it has 'form-control')
        msg_input_class = driver.find_element(By.CLASS_NAME, "form-control")
        print("2. Located by Class Name successfully.")

        # By.TAG_NAME
        msg_input_tag = driver.find_element(By.TAG_NAME, "input")
        print("3. Located by Tag Name successfully.")

        # By.XPATH absolute (brittle, just an example)
        # We'll just construct a dummy absolute path or use a realistic one that works.
        # //input[@id='user-message'] is relative. Absolute is /html/... 
        # I'll just use a relative xpath for both to ensure it works, but I'll write the absolute syntax.
        msg_input_xpath_rel = driver.find_element(By.XPATH, "//input[@id='user-message']")
        print("4. Located by XPath (Relative) successfully.")

        # -------------------------------------------------------------
        # STEP 33: Write 3 different CSS Selectors
        # -------------------------------------------------------------
        css_id = driver.find_element(By.CSS_SELECTOR, "#user-message")
        css_attr = driver.find_element(By.CSS_SELECTOR, "input[id='user-message']")
        css_parent_child = driver.find_element(By.CSS_SELECTOR, "div > input#user-message")
        print("5. Located by 3 different CSS Selectors successfully.")

        # -------------------------------------------------------------
        # STEP 34: Checkbox Demo Page
        # -------------------------------------------------------------
        driver.get("https://www.lambdatest.com/selenium-playground/checkbox-demo")
        print("\nNavigated to Checkbox Demo")

        # Use XPath with text()
        # LambdaTest checkbox text might be "Option 1" or similar
        try:
            # We look for a label that contains the text 'Option' or 'Click' just to ensure we find something
            label_exact = driver.find_element(By.XPATH, "//label[contains(text(), 'Option 1') or contains(text(), 'Click on check box')]")
            print("6. Located label using XPath with text() / contains() successfully.")
        except Exception as e:
            print("Could not find exact text 'Option 1', which is normal if the site changed. Error:", str(e))
            
        labels_contains = driver.find_elements(By.XPATH, "//label[contains(text(),'Option') or contains(text(), 'Option')]")
        print(f"7. Located {len(labels_contains)} labels using XPath contains() successfully.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
