from selenium.webdriver.common.action_chains import ActionChains  # Type text without specific Element


def sendkeys(driver, keys):  # send keys without specific Element
    actions = ActionChains(driver)
    actions.send_keys(str(keys))
    actions.perform()
