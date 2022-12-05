from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


def touch_action_chain(driver):
    """
    credits: https://www.reddit.com/r/Appium/comments/rbx1r2/touchaction_deprecated_please_use_w3c_i_stead/

    actions = touch_action_chain(driver)
    actions.pointer_action.move_to_location(mid_location['x'],mid_location['y'])
    actions.pointer_action.click()
    actions.perform()
    """
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    return actions.w3c_actions

# noinspection PyShadowingNames
def mid_location(element):
    return {'x': element.location_once_scrolled_into_view['x'] + (element.rect["width"] / 2),
     'y': element.location_once_scrolled_into_view['y'] + (element.rect["height"] / 2)}


