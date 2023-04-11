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


def config_options(options, adb=False, dublicate_policy="warn-replace"):
    from selenium_profiles.scripts.profiles import options as option_manager
    manager = option_manager(options)
    if "excludeSwitches" in options.experimental_options.keys():
        if "enable-automation" not in options.experimental_options["excludeSwitches"]:
            manager.Options.experimental_options["excludeSwitches"].append("enable-automation")
    else:
        manager.update_experimental_options({"excludeSwitches": ["enable-automation"]}, dublicate_policy=dublicate_policy)
    if not adb or adb is None:
        manager.update_experimental_options({'useAutomationExtension': False}, dublicate_policy=dublicate_policy)
    manager.extend_arguments(["--disable-blink-features=AutomationControlled", "--disable-blink-features"], dublicate_policy="warn-add")

    # suppress welcome
    manager.extend_arguments(["--no-default-browser-check", "--no-first-run"], dublicate_policy="warn-add")

    return manager.Options
