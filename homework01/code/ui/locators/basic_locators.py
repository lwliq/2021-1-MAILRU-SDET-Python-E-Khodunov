from selenium.webdriver.common.by import By

LOAD_SPINNER_LOCATOR = (By.CLASS_NAME, 'spinner')
RIGHT_PROFILE_BUTTON_LOCATOR = (By.CLASS_NAME, 'right-module-rightWrap-3lL6mf')
LOGOUT_BUTTON = (By.XPATH, '//a[text()="Выйти" and @href="/logout"]')

INSTRUCTION_MODULE_LOCATOR = (By.CLASS_NAME, 'instruction-module-container-HuFj-l')
PROFILE_RIBBON_BUTTON = (By.CLASS_NAME, 'center-module-profile-BHql9z')
SEGMENTS_RIBBON_BUTTON = (By.CLASS_NAME, 'center-module-segments-3y1hDo')
BILLING_RIBBON_BUTTON = (By.CLASS_NAME, 'center-module-billing-x3wyL6')

SEGMENTS_LABEL_LOCATOR = (By.CLASS_NAME, 'left-nav__group__label')
BILLING_TITLE_LOCATOR = (By.CLASS_NAME, 'deposit__payment-form__title')