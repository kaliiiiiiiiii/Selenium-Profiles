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

class requests:
    def __init__(self, driver):
        self.driver = driver
        self.methods = ["GET","HEAD" "POST", "PUT", "DELETE","OPTIONS"] # TRACE, CONNECT exluded here
        self.supported_credentials = ["omit", "same-origin", "include"]
        self.modes = ["cors", "no-cors", "same-origin"]
        self.cache_values = ["default", "no-store", "reload", "no-cache", "force-cache", "only-if-cached"]
        self.redirect_values = ["follow", "error"] # "manual" excluded here
        self.referrer_policies = ["no-referrer", "no-referrer-when-downgrade", "same-origin", "origin", "strict-origin", "origin-when-cross-origin", "strict-origin-when-cross-origin", "unsafe-url"]
        self.priorities = ["high", "low", "auto"]
    def fetch(self, url: str,
              method="GET",
              headers:dict=None,
              body:str or object=None,
              mode:str=None,
              credentials:str="same-origin",
              cache:str="no-cache",
              redirect="follow",
              referrer=None,
              referer_policy = None,
              priority="high"
                    ):
        import json
        from selenium_profiles.utils.utils import read
        import codecs

        options = {}
        if method:
            self.check_cmd(method, self.methods)
            options["method"] = method
        if headers:
            options["headers"] = headers
        if body:
            if method in ["GET", "HEAD"]:
                raise ValueError("body can't be used with GET or HEAD method")
            options["body"] = body
        if mode:
            self.check_cmd(mode, self.modes)
            options["mode"] = mode
        if credentials:
            self.check_cmd(credentials, self.supported_credentials)
            options["credentials"] = credentials
        if cache:
            self.check_cmd(cache, self.cache_values)
            options["cache"] = cache
        if redirect:
            self.check_cmd(redirect, self.redirect_values)
            options["redirect"] = redirect
        if referrer:
            options["referrer"] = referrer
        if referer_policy:
            self.check_cmd(referer_policy,self.referrer_policies)
            options['referrerPolicy'] = referer_policy
        if priority:
            options["priority"] = priority



        options = json.dumps(options)
        url = json.dumps(url)
        js = read("js/fetch.js", sel_root=True) % (url, options)
        response = self.driver.execute_async_script(js)
        if response["status"] == "200":
            response = response["value"]
            response["content"] = codecs.decode(response["HEX"], "hex")
            response["text"] = response["content"].decode("utf-8")
            del response["HEX"]
        elif response["status"] == "error":
            raise Exception(response["stack"])

        # https://developer.mozilla.org/en-US/docs/Web/API/fetch#syntax
        return response

    def check_cmd(self, value, values):
        if value not in values:
            raise ValueError("got "+str(value)+" , but expected "+str(values))
