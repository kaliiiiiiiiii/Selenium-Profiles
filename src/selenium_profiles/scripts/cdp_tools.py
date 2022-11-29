from typing import Dict, List  # define types in functions
import warnings
import json


# noinspection PyPep8Naming
class cdp_tools(object):
    def __init__(self, driver):
        self.driver = driver

        # initial property
        self.evaluate_on_document_identifiers = {}

    # EMULATION

    def set_emulation(self, emulation, enabled=True) -> (Dict[str, int or Dict[str, str or int or float]], bool):
        emulation.update({"mobile": enabled})
        if enabled:
            warnings.warn('disabling emulation not supported')
            x = self.driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', emulation)
            return self.driver.execute_cdp_cmd('Page.setDeviceMetricsOverride', emulation), x

    def set_useragent(self, useragent) -> Dict[str, str or Dict[str, str or bool or List[Dict[str, str]]]]:
        x = self.driver.execute_cdp_cmd('Emulation.setUserAgentOverride', useragent)
        # noinspection PyTypeChecker
        return self.driver.execute_cdp_cmd("Network.setUserAgentOverride", useragent), x

    # BROWSER

    def set_darkmode(self, enabled=True, mobile=True) -> (bool, bool):
        if not mobile and enabled:
            warnings.warn('darkmode might look weird without mobile_view!')
        else:
            return self.driver.execute_cdp_cmd('Emulation.setAutoDarkModeOverride',
                                               {'enabled': enabled})

    # TOUCH

    def set_touchpoints(self, enabled=True, maxpoints=5) -> (bool, int):  # set touch options
        return self.driver.execute_cdp_cmd('Emulation.setTouchEmulationEnabled',
                                           {'enabled': enabled, 'maxTouchPoints': maxpoints})  # already set in options

    def pointer_as_touch(self, mobile, enabled=True) -> (bool, bool):  # (makes code hung)
        if mobile:
            config = 'mobile'
        else:
            config = 'desktop'
        if enabled:
            warnings.warn('Actions execute, but then take long when "EmitTouchEventsForMouse"!')
        return self.driver.execute_cdp_cmd('Emulation.setEmitTouchEventsForMouse', {'enabled': enabled,
                                                                                    'configuration': config})  # executes, but then takes long [maybe check if success?]

    # OVERRIDE JAVASCRIPT

    def evaluate_on_new_document(self, js: str):  # evaluate js on every new page
        identifier = int(
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})["identifier"])
        self.evaluate_on_document_identifiers.update({identifier: js})
        return identifier

    # remove js evaluation  on every new page for specific script
    def remove_evaluate_on_document(self, identifier: int):
        del self.evaluate_on_document_identifiers[identifier]
        return self.driver.execute_cdp_cmd("Page.removeScriptToEvaluateOnNewDocument", {"identifier": str(identifier)})

    # define var.property for javascript
    def define_prop_on_new_document(self, var, prop, val, func='get: ()') -> (str, str, any, str):
        self.evaluate_on_new_document(
            "Object.defineProperty(" + var + ", " + json.dumps(prop) + ", {" + func + " => " + json.dumps(val) + "})")

    # COOKIES

    def get_cookies(self):
        return self.driver.execute_cdp_cmd("Network.getAllCookies", {})

    def get_cookie(self, urls: list = []):
        if len(urls) > 0:
            arg = {"urls": urls}
        else:
            arg = {}
        return self.driver.execute_cdp_cmd("Network.getCookies", arg)

    def add_cookie(self, cookie_dict):
        return self.driver.execute_cdp_cmd("Network.setCookie", cookie_dict)

    def delete_cookie(self, name: str):
        return self.driver.execute_cdp_cmd("Network.deleteCookies", {"name": name})

    def delete_all_cookies(self):
        return self.driver.execute_cdp_cmd("Network.clearBrowserCookies", {})
