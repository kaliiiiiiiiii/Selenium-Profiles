from selenium_profiles.utils.utils import read


def exec_cdp(driver, cdp_tools=None):
    if cdp_tools:
        do_return = False
    else:
        from selenium_profiles.scripts.cdp_tools import cdp_tools
        cdp_tools = cdp_tools(driver)
        do_return = True

    # set webdriver js var to false
    cdp_tools.evaluate_on_new_document(read('js/undetected/navigator_webdriver.js'))

    # noinspection PyUnusedLocal
    x = driver.execute_cdp_cmd('Emulation.setIdleOverride', {'isUserActive': True, 'isScreenUnlocked': True})

    def get_cdc_props():  # if true ==> detectable
        return driver.execute_script(read('js/undetected/get_cdc_props.js'))

    if get_cdc_props():
        # remove cdc-props:)
        # cdp_tools.evaluate_on_new_document(read('js/undetected/remove_cdc_props.js'))
        cdp_tools.remove_evaluate_on_document(1)

        if do_return:
            return cdp_tools.evaluate_on_document_identifiers


def config_options(options, adb=False):
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    if not adb or adb is None:
        options.add_experimental_option('useAutomationExtension', False)
    options.arguments.extend(["--disable-blink-features=AutomationControlled", "--disable-blink-features"])

    # suppress welcome
    options.arguments.extend(["--no-default-browser-check", "--no-first-run"])

    return options
