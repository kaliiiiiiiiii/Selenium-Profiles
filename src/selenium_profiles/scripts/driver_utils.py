import warnings

from selenium.webdriver.common.action_chains import ActionChains  # Type text without specific Element


class actions(object):
    def __init__(self, driver):
        self.driver = driver
    def sendkeys(self, keys):  # send keys without specific Element
        action = ActionChains(self.driver)
        action.send_keys(str(keys))
        action.perform()

    def touch_action_chain(self):
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.common.actions import interaction
        from selenium.webdriver.common.actions.action_builder import ActionBuilder
        from selenium.webdriver.common.actions.pointer_input import PointerInput
        """
        credits: https://www.reddit.com/r/Appium/comments/rbx1r2/touchaction_deprecated_please_use_w3c_i_stead/

        actions = touch_action_chain(driver)
        actions.pointer_action.move_to_location(mid_location['x'],mid_location['y'])
        actions.pointer_action.click()
        actions.perform()
        """
        action = ActionChains(self.driver)
        action.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        return action.w3c_actions
    def mid_location(self, element):
        return {'x': element.location_once_scrolled_into_view['x'] + (element.rect["width"] / 2),
                'y': element.location_once_scrolled_into_view['y'] + (element.rect["height"] / 2)}

class requests(object):
    def __init__(self, driver):
        self.driver = driver
    def fetch(self, url: str, options: dict or None = None):
        import json
        if options is None:
            options = {'headers': {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,fr;q=0.5,de-CH;q=0.4',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'sec-ch-ua': "'Not_A Brand';v='99', 'Microsoft Edge';v='109', 'Chromium';v='109'",
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': "'Windows'",
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                "cookie": ''
            },
                'referrerPolicy': 'strict-origin-when-cross-origin',
                'body': None,
                'method': 'GET'
            }
        options = json.dumps(options)
        js = """
            var done = arguments[0];
            fetch('%s', %s,).then(response=>response.json())
                            .then(data=>{ done(data) })
                        """ % (url, options)

        # https://developer.mozilla.org/en-US/docs/Web/API/fetch#syntax
        return self.driver.execute_async_script(js)