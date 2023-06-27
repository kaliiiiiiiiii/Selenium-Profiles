from selenium_profiles.utils.utils import read


def exec_cdp(driver, cdp_handler = None):
    if not cdp_handler:
        if "profiles" in driver.__dir__():
            cdp_handler = driver.profiles.cdp_handler
        else:
            from selenium_profiles.scripts.profiles import cdp_handler
            cdp_handler = cdp_handler(driver=driver)

    # set webdriver js var to false
    cdp_handler.evaluate_on_new_document(read('js/undetected/navigator_webdriver.js'))

    driver.execute_cdp_cmd('Emulation.setIdleOverride', {'isUserActive': True, 'isScreenUnlocked': True})

    cdp_handler.remove_evaluate_on_document(1)


def config_options(options, adb=False, duplicate_policy="warn-replace"):
    from selenium_profiles.scripts.profiles import options as option_manager
    manager = option_manager(options)
    if "excludeSwitches" in options.experimental_options.keys():
        if "enable-automation" not in options.experimental_options["excludeSwitches"]:
            manager.Options.experimental_options["excludeSwitches"].append("enable-automation")
    else:
        manager.update_experimental_options({"excludeSwitches": ["enable-automation"]}, duplicate_policy=duplicate_policy)
    if not adb or adb is None:
        manager.update_experimental_options({'useAutomationExtension': False}, duplicate_policy=duplicate_policy)
    manager.extend_arguments(["--disable-blink-features=AutomationControlled"], duplicate_policy="warn-add")

    # suppress welcome
    manager.extend_arguments(["--no-default-browser-check", "--no-first-run"], duplicate_policy="warn-add")

    return manager.Options
