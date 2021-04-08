from selenium.webdriver.common.by import By


class BasePageLocators:
    pass


class LoginPageLocators:
    LOGIN_BUTTON_LOCATOR = (By.CSS_SELECTOR, 'div[class*="responseHead-module-button"]')
    EMAIL_INPUT_LOCATOR = (By.NAME, 'email')
    PASSWORD_INPUT_LOCATOR = (By.NAME, 'password')
    SUBMIT_BUTTON_LOCATOR = (By.CSS_SELECTOR, 'div[class*=authForm-module-button]')
    TARGET_ERROR_NOTIFICATION = (By.CSS_SELECTOR, 'div[class*=notify-module-error]')
    MYCOM_ERROR_NOTIFICATION = (By.CLASS_NAME, 'formMsg_text')


class DashboardPageLocators:
    RIGHT_PROFILE_BUTTON_LOCATOR = (By.CSS_SELECTOR, 'div[class*=right-module-rightWrap]')
    LOGOUT_BUTTON = (By.XPATH, '//a[text()="Выйти" and @href="/logout"]')

    INSTRUCTION_MODULE_LOCATOR = (By.CSS_SELECTOR, 'div[class*=instruction-module-container]')
    PROFILE_RIBBON_BUTTON = (By.CSS_SELECTOR, 'a[class*=center-module-profile]')
    SEGMENTS_RIBBON_BUTTON = (By.CSS_SELECTOR, 'a[class*=center-module-segments]')

    NEW_CAMPAIGN_INSTRUCTIONS_LINK = (
        By.XPATH,
        '//div[contains(@class, "instruction")]//a[@href="/campaign/new"]'
    )
    NEW_CAMPAIGN_BUTTON = (
        By.XPATH,
        '//div[contains(@class, "button") and contains(text(), "Создать кампанию")]'
    )
    CAMPAIGN_COLLAPSE_BUTTON_TEMPLATE = (
        By.XPATH,
        '//div[@data-entity-type="campaign"]//a[@title="{}"]/../div[contains(@class, "hasChildren")]'
    )
    BANNER_SELECT_CHECKBOX_TEMPLATE = (
        By.XPATH,
        '//div[@data-entity-type="banner"]//div[@title="{}"]/../input[@type="checkbox"]'
    )
    CAMPAIGN_SELECT_CHECKBOX_TEMPLATE = (
        By.XPATH,
        '//div[@data-entity-type="campaign"]//a[@title="{}"]/../input[@type="checkbox"]'
    )
    CAMPAIGN_CELL_TEMPLATE = (
        By.XPATH,
        '//div[@data-entity-type="campaign"]//a[@title="{}"]/ancestor::div[contains(@class, "CellFirst")]'
    )
    BANNER_CELL_TEMPLATE = (
        By.XPATH,
        '//div[@data-entity-type="banner"]//div[@title="{}"]/ancestor::div[contains(@class, "CellFirst")]'
    )

    TABLE_CONTROLS_SELECT = (
        By.XPATH,
        '//div[@data-test="select" and contains(@class, "tableControls")]'
    )
    SELECT_LIST_ITEM_TEMPLATE = (
        By.XPATH,
        '//ul[@data-test="select_list"]//li[@title="{}"]'
    )

    class Table:
        STATUS_CELL_TEMPLATE = (
            By.XPATH,
            '//div[contains(@data-test, "status-{}")]//span[contains(@class, "statusText")]'
        )


class SegmentsPageLocators:
    NEW_SEGMENT_INSTRUCTIONS_LINK = (
        By.XPATH,
        '//div[contains(@class, "instruction")]//a[@href="/segments/segments_list/new/"]'
    )
    NEW_SEGMENT_BUTTON = (
        By.XPATH,
        '//div[contains(@class, "segments-list")]//button[@data-class-name="Submit"]'
    )
    SEGMENTS_CATEGORY_TEMPLATE = (
        By.XPATH,
        '//div[@data-class-name="SourcesFormView"]//div[@data-class-name="TypeItemView" and text()="{}"]'
    )
    SEGMENT_CHECKBOX_TEMPLATE = (
        By.XPATH,
        '//span[contains(@class, "source-name") and text()="{}"]/'
        'ancestor::div[@class="adding-segments-source"]//input[contains(@class, "adding-segments-source")]'
    )
    ADD_SEGMENT_BUTTON = (
        By.XPATH,
        '//div[contains(@class, "adding-segments")]//button[@data-class-name="Submit"]'
    )
    SEGMENT_NAME_INPUT = (
        By.XPATH,
        '//div[contains(@class, "segment-name")]//input'
    )
    CREATE_SEGMENT_BUTTON = (
        By.XPATH,
        '//div[contains(@class, "create-segment-form")]//button[@data-class-name="Submit"]'
    )
    CONFIRM_REMOVE_BUTTON = (
        By.XPATH,
        '//div[@data-class-name="Confirm"]//button[contains(@class, "button_confirm-remove")]'
    )

    class Table:
        TITLE_CELL_TEMPLATE = (
            By.XPATH,
            '//a[@title="{}"]/../..'
        )
        CHECKBOX_TEMPLATE = (
            By.XPATH,
            '//div[contains(@data-test, "id-{}")]//input[@type="checkbox"]'
        )
        REMOVE_BUTTON_TEMPLATE = (
            By.XPATH,
            '//div[contains(@data-test, "remove-{}")]/span'
        )


class NewCampaignPageLocators:
    OBJECTIVE_BUTTON_TEMPLATE = (
        By.XPATH,
        '//div[contains(@class, "objectives-wrap")]//div[contains(@class, "_{}")]'
    )

    URL_INPUT = (By.XPATH, '//div[contains(@class, "main-url-wrap")]//input')
    CAMPAIGN_NAME_INPUT = (By.XPATH, '//div[@class="campaign-name"]//input')

    EXPANDABLE_MENU_TEMPLATE = (
        By.XPATH,
        '//div[@data-targeting="{}"]'
    )

    CAMPAIGN_SUBMIT_BUTTON = (
        By.XPATH,
        '//div[@data-class-name="FooterView"]//button[@data-class-name="Submit"]'
    )

    class Targeting:

        SEX_CHECKBOX_TEMPLATE = (By.XPATH, '//input[contains(@targeting, "{}")]')

        AGE_SELECT_MENU = (By.XPATH, '//div[contains(@class, "age-setting-select")]')
        AGE_SELECT_ITEM_TEMPLATE = (
            By.XPATH,
            '//div[contains(@class, "age-setting-select")]//li[@data-id="{}"]'
        )
        AGE_CUSTOM_TEXTAREA = (By.XPATH, '//div[contains(@class, "age-setting__text")]//textarea')

        GEO_REGION_INPUT = (By.XPATH, '//div[contains(@class, "region-module-selectors")]//input')
        GEO_REGION_ADD_BUTTON_TEMPLATE = (
            By.XPATH,
            '//li[@title="{}"]//div[contains(text(), "Добавить")]'
        )
        GEO_REGION_EXCLUDE_BUTTON_TEMPLATE = (
            By.XPATH,
            '//li[@title="{}"]//div[contains(text(), "Исключить")]'
        )
        GEO_SELECTED_REGIONS_REMOVE_TEMPLATE = (
            By.XPATH,
            '//span[@title="{}"]/../span[contains(@class, "itemClose")]'
        )
        GEO_SELECTED_REGIONS_SWITCH_TEMPLATE = (
            By.XPATH,
            '//span[@title="{}"]/ancestor::div[contains(@class, "selectedRegions-module-item")]/label'
        )

        INTERESTS_SOC_DEM_GROUP_COLLAPSE_TEMPLATE = (
            By.XPATH,
            '//li[@data-setting-name="interests_soc_dem"]//label[@title="{}"]/..'
            '/span[contains(@class, "collapse-icon")]'
        )
        INTERESTS_SOC_DEM_GROUP_ITEM_CHECKBOX_TEMPLATE = (
            By.XPATH,
            '//li[@data-setting-name="interests_soc_dem"]//label[@title="{}"]/../input[@type="checkbox"]'
        )

        INTERESTS_GROUP_COLLAPSE_TEMPLATE = (
            By.XPATH,
            '//li[@data-setting-name="interests"]//label[@title="{}"]/..'
            '/span[contains(@class, "collapse-icon")]'
        )
        INTERESTS_GROUP_ITEM_CHECKBOX_TEMPLATE = (
            By.XPATH,
            '//li[@data-setting-name="interests"]//label[@title="{}"]/../input[@type="checkbox"]'
        )

    class WhenTargeting:

        FULL_TIME_SETTING_PRESET_TEMPLATE = (
            By.XPATH,
            '//li[@data-name="fulltime"]//li[@data-name="{}"]'
        )
        DATE_INPUT_TEMPLATE = (
            By.XPATH,
            '//li[@data-name="date"]//div[contains (@class, "{}")]/input'
        )

    class BudgetTargeting:

        BUDGET_INPUT_TEMPLATE = (
            By.XPATH,
            '//li[@data-setting-name="budget_setting"]//input[@data-test="{}"]'
        )

    class BannerFormats:

        BANNER_FORMAT_TEMPLATE = (
            By.XPATH,
            '//div[@data-class-name="BannerSettingsView"]//span[text()="{}"]'
        )

    class BannerEditor:

        BANNER_IMAGE_INPUT_TEMPLATE = (
            By.XPATH,
            '//div[contains(@class, "editorForm")]//input[@data-test="{}"]'
        )
        IMAGE_CROPPER_SUBMIT_BUTTON = (By.XPATH, '//div[@class="image-cropper"]//input[@type="submit"]')
        BANNER_TITLE_INPUT = (By.XPATH, '//div[contains(@class, "editorForm")]//input[contains(@data-name, "title")]')
        BANNER_TEXT_INPUT_TEMPLATE = (
            By.XPATH,
            '//div[contains(@class, "editorForm")]//textarea[contains(@data-name, "{}")]'
        )
        BANNER_NAME_INPUT = (By.XPATH, '//div[contains(@class, "editorForm")]//input[@data-name="banner-name"]')
        BANNER_SUBMIT_BUTTON = (
            By.XPATH,
            '//div[contains(@class, "bannerEditor")]/div[@data-test="submit_banner_button"]'
        )
