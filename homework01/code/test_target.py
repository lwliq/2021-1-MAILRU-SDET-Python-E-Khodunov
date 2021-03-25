import pytest
from base import BaseCase
from ui.locators import basic_locators
from ui.locators import login_locators
from ui.locators import profile_locators
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys


class TestOne(BaseCase):
    @pytest.mark.UI
    def test_login(self, login, logout):
        instruction_module = self.find(basic_locators.INSTRUCTION_MODULE_LOCATOR)
        assert instruction_module.is_displayed()

    @pytest.mark.UI
    def test_logout(self, login):
        self.click(basic_locators.RIGHT_PROFILE_BUTTON_LOCATOR)
        self.click(basic_locators.LOGOUT_BUTTON, 15)
        login_button = self.find(login_locators.LOGIN_BUTTON_LOCATOR, 15)
        assert login_button.is_displayed()

    @pytest.mark.UI
    def test_change_profile(self, login, logout):
        self.spinner_wait(timeout=1)
        self.click(basic_locators.PROFILE_RIBBON_BUTTON)

        fio = "Иванов Иван Иванович"
        phone = "1112223344"
        email = "test@test.com"

        self.input_text(
            text=fio,
            locator=profile_locators.FIO_INPUT_LOCATOR
        )

        self.input_text(
            text=phone,
            locator=profile_locators.PHONE_INPUT_LOCATOR
        )

        self.input_text(
            text=email,
            locator=profile_locators.EMAIL_INPUT_LOCATOR
        )

        self.click(profile_locators.SAVE_BUTTON_LOCATOR)
        self.wait().until(
            expected_conditions.visibility_of_element_located(profile_locators.SUCCESS_NOTIFICATION_LOCATOR)
        )

        self.driver.refresh()

        assert (
            fio == self.find(profile_locators.FIO_INPUT_LOCATOR).get_attribute('value') and
            phone == self.find(profile_locators.PHONE_INPUT_LOCATOR).get_attribute('value') and
            email == self.find(profile_locators.EMAIL_INPUT_LOCATOR).get_attribute('value')
        )

        # clear() очищает поля, но изменения не сохраняются, поэтому такой костыль
        fio = self.find(profile_locators.FIO_INPUT_LOCATOR)
        fio.clear()
        fio.send_keys(Keys.SPACE, Keys.BACK_SPACE)
        phone = self.find(profile_locators.PHONE_INPUT_LOCATOR)
        phone.clear()
        phone.send_keys(Keys.SPACE, Keys.BACK_SPACE)
        email = self.find(profile_locators.EMAIL_INPUT_LOCATOR)
        email.clear()
        email.send_keys(Keys.SPACE, Keys.BACK_SPACE)

        self.click(profile_locators.SAVE_BUTTON_LOCATOR)
        self.wait().until(
            expected_conditions.visibility_of_element_located(profile_locators.SUCCESS_NOTIFICATION_LOCATOR)
        )

    @pytest.mark.UI
    @pytest.mark.parametrize(
        'button_locator, expected_locator, expected_value',
        [
            pytest.param(
                basic_locators.SEGMENTS_RIBBON_BUTTON,
                basic_locators.SEGMENTS_LABEL_LOCATOR,
                'Аудиторные сегменты'
            ),
            pytest.param(
                basic_locators.BILLING_RIBBON_BUTTON,
                basic_locators.BILLING_TITLE_LOCATOR,
                'Плательщик'
            )
        ]
    )
    def test_pages(self, login, logout, button_locator, expected_locator, expected_value):
        self.click(button_locator)
        element = self.find(expected_locator)
        assert expected_value == element.get_attribute('innerHTML')
