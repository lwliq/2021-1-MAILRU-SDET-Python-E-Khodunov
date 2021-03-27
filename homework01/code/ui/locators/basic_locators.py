from selenium.webdriver.common.by import By

LOAD_SPINNER_LOCATOR = (By.CLASS_NAME, 'spinner')
RIGHT_PROFILE_BUTTON_LOCATOR = (By.CSS_SELECTOR, 'div[class*=right-module-rightWrap]')
LOGOUT_BUTTON = (By.XPATH, '//a[text()="Выйти" and @href="/logout"]')

INSTRUCTION_MODULE_LOCATOR = (By.CSS_SELECTOR, 'div[class*=instruction-module-container]')
PROFILE_RIBBON_BUTTON = (By.CSS_SELECTOR, 'a[class*=center-module-profile]')
SEGMENTS_RIBBON_BUTTON = (By.CSS_SELECTOR, 'a[class*=center-module-segments]')
BILLING_RIBBON_BUTTON = (By.CSS_SELECTOR, 'a[class*=center-module-billing]')

SEGMENTS_LABEL_LOCATOR = (By.CLASS_NAME, 'left-nav__group__label')
BILLING_TITLE_LOCATOR = (By.CLASS_NAME, 'deposit__payment-form__title')
