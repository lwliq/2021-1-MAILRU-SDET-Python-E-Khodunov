from selenium.webdriver.common.by import By

LOGIN_BUTTON_LOCATOR = (By.CSS_SELECTOR, 'div[class*="responseHead-module-button"]')
EMAIL_INPUT_LOCATOR = (By.NAME, 'email')
PASSWORD_INPUT_LOCATOR = (By.NAME, 'password')
SUBMIT_BUTTON_LOCATOR = (By.CSS_SELECTOR, 'div[class*=authForm-module-button]')
