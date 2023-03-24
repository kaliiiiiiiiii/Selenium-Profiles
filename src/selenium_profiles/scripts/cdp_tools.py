from typing import Dict, List  # define types in functions
import warnings
import json
import traceback


# noinspection PyPep8Naming
class cdp_tools(object):
    def __init__(self, driver):
        self.driver = driver

        # initial property
        self.evaluate_on_document_identifiers = {}

    # EMULATION

    def set_emulation(self, emulation:bool or None) -> (Dict[str, int or Dict[str, str or int or float]]):
        if emulation:
            return self.driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', emulation)

    def clear_emulation(self, enabled:bool or None):
        if enabled or (enabled is None):
            self.driver.execute_cdp_cmd("Emulation.clearDeviceMetricsOverride", {})

    def set_useragent(self, useragent) -> Dict[str, str or Dict[str, str or bool or List[Dict[str, str]]]] or None:
        if useragent:
            return self.driver.execute_cdp_cmd('Emulation.setUserAgentOverride', useragent)

    def set_cores(self, cores_count:int or None=8):
        if cores_count:
            return self.driver.execute_cdp_cmd("Emulation.setHardwareConcurrencyOverride", {"hardwareConcurrency":cores_count})

    # BROWSER

    def set_darkmode(self, enabled=True, mobile=True) -> (bool, bool):
        if not (mobile or mobile is None) and enabled:
            warnings.warn('darkmode might look weird without mobile_view!')
        if enabled:
            return self.driver.execute_cdp_cmd('Emulation.setAutoDarkModeOverride',
                                           {'enabled': enabled})

    # TOUCH

    def set_touchpoints(self, enabled:bool or None=True, maxpoints:int or None=10):  # set touch options
        if maxpoints is None:
            maxpoints = 10
        return self.driver.execute_cdp_cmd('Emulation.setTouchEmulationEnabled',
                                           {'enabled': enabled, 'maxTouchPoints': maxpoints})  # already set in options

    def pointer_as_touch(self, mobile:bool or None, enabled:bool or None=True):  # (makes code hung)
        if mobile or mobile is None:
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

    def get_cookie(self, urls: list = None):
        if urls:
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
