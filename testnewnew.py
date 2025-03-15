from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# ✅ Constants
BASE_URL = "https://demo.spikerz.com"
SOCIAL_CONNECT_URL = f"{BASE_URL}/social-connect"

# ✅ Credentials
SPIKERZ_USERNAME = "me"
SPIKERZ_PASSWORD = "SmipMe123456"
GOOGLE_EMAIL = "your-email@gmail.com"
GOOGLE_PASSWORD = "yourpasswrod"

# ✅ Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--disable-web-security")  # Disable security for cross-origin issues
options.add_argument("--start-maximized")  # Maximize the browser window

# ✅ Initialize WebDriver with proper setup
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# ✅ Define an explicit wait
wait = WebDriverWait(driver, 20)

# ✅ Step 1: Open Spikerz & Handle Authentication Popup
driver.get(f"https://{SPIKERZ_USERNAME}:{SPIKERZ_PASSWORD}@demo.spikerz.com")
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))  # Ensure the page has loaded

# ✅ Step 2: Navigate to Social Connect Page
driver.get(SOCIAL_CONNECT_URL)

# ✅ Step 3: Click YouTube Connect Button
youtube_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@class='ng-tns-c3906472781-2 platform-icon platform-youtube']")))
youtube_button.click()
print("ℹ️ Clicked YouTube button")

# ✅ Step 4: Click the YouTube authentication dropdown button
youtube_auth_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-dropdown-trigger button-body image-only default ant-btn-default']")))
youtube_auth_button.click()
print("ℹ️ Clicked YouTube authentication dropdown button")

# ✅ Step 5: Handle Google Authentication in New Window
main_window = driver.current_window_handle  # Store the current window handle
wait.until(lambda d: len(driver.window_handles) > 1)  # Wait for the new window to open

# ✅ Switch to Google login window
for window in driver.window_handles:
    if window != main_window:
        driver.switch_to.window(window)
        break
print("ℹ️ Switched to Google login window")

# ✅ Step 6: Google Login - Enter Email
wait.until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys(GOOGLE_EMAIL + Keys.RETURN)
time.sleep(2)  # Wait for password field to load

# ✅ Enter Password
password_field = wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
password_field.send_keys(GOOGLE_PASSWORD + Keys.RETURN)
print("ℹ️ Entered Google credentials")

# ✅ Step 7: Handle Google Consent Screen (if shown)
approve_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continue')]")))
approve_button.click()
print("ℹ️ Clicked 'Continue' button on Google consent screen")

try:
    # ✅ Step 8: Handle Checkbox Selection (if required)
    checkbox = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox' and @id='i1']")))
    driver.execute_script("arguments[0].click();", checkbox)  # Click using JavaScript in case it's hidden
    print("ℹ️ Selected the checkbox")
except:
    print("ℹ️ Checkbox not found, skipping to Continue button...")

# ✅ Click Continue Button
approve_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continue')]")))
approve_button.click()
print("ℹ️ Clicked 'Continue' button on Google consent screen")

# ✅ Step 9: Switch Back to Main Window
driver.switch_to.window(main_window)

# ✅ Step 10: Verify Success Message
# ✅ Validate the presence of '@dina_bakery_shop' on the page
element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '@dina_bakery_shop')]")))
assert element.text == "@dina_bakery_shop", "Text validation failed!"
print("✅ Text '@dina_bakery_shop' is present on the page!")

# ✅ Quit the browser
driver.quit()
