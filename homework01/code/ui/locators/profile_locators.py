from selenium.webdriver.common.by import By

FIO_INPUT_LOCATOR = (By.XPATH, '//div[@data-name="fio"]/div/input')
PHONE_INPUT_LOCATOR = (By.XPATH, '//div[@data-name="phone"]/div/input')
EMAIL_INPUT_LOCATOR = (By.XPATH, '//div[@data-class-name="AdditionalEmailRow"]/div/div/div/input')

SAVE_BUTTON_LOCATOR = (By.CLASS_NAME, 'button_submit')
SUCCESS_NOTIFICATION_LOCATOR = (By.XPATH, '//div[@data-class-name="SuccessView"]')