import warnings
import undetected_chromedriver as uc  # undetected chromedriver
from selenium.webdriver.common.action_chains import ActionChains  # Type text without specific Element
from utils import read  # read txt files
import traceback  # print exception
from typing import Dict, List  # define types in functions
import json  # python dict to js


def sendkeys(driver, keys):  # send keys without specific Element
    actions = ActionChains(driver)
    actions.send_keys(str(keys))
    actions.perform()


# noinspection PyPep8Naming,GrazieInspection
class driver(object):
    def __init__(self):
        # initial attributes
        self.returnnavigator = None
        self.profile = None
        self.driver = None
        self.js_return_navigator = read('get_navigator.js')[0]  # for exporting javascript Variables

    def start(self, profile: Dict[str, dict or list]):
        self.profile = profile
        mobile = profile['device']['mobile']

        if not profile["plugins"]["selenium-wire"] is False:
            warnings.warn("Selenium-wire not supported yet, ignoring")

        options = uc.ChromeOptions()  # selenium.webdriver options, https://peter.sh/experiments/chromium-command-line-switches/

        # always used options
        size = profile["browser"]["window_size"]
        options.add_argument("--window-size=" + str(size["x"]) + "," + str(size["y"]))
        options.add_argument('--user-agent=' + profile["device"]["agent_override"]["userAgent"])
        options.set_capability("platformName", profile["device"]["agent_override"]["userAgentMetadata"][
            "platform"])  # todo does it have an effect?
        options.arguments.extend(["--no-default-browser-check", "--no-first-run"])
        options.arguments.extend(["--disable-blink-features=AutomationControlled", "--disable-blink-features"])
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option('useAutomationExtension', False)

        # options-manager
        if not profile["browser"]["sandbox"]:
            options.arguments.extend(["--no-sandbox", "--test-type"])
        if profile["browser"]["headless"]:
            options.add_argument('--headless')
        if profile["browser"]["touch_events"]:
            options.add_argument("--touch-events=enabled")
        if profile["browser"]["app"]:
            options.add_argument('--app')
            options.add_argument('--force-app-mode')
        if profile["device"]["touch_device"]:
            options.add_argument("--touch-events=enabled")  # enable touch events
        if profile["browser"]["inkognito"]:
            options.add_argument("--incognito")
        if not profile["device"]['hardware_accel']:
            options.add_argument('--disable-gpu')
            options.add_argument('--override-use-software-gl-for-tests')
        if mobile:
            options.add_argument('--arc-availability=officially-supported')
            options.add_argument('--force-device-ownership')
            options.add_argument('--enable-features=enable-nacl')
            options.add_argument('--use-mobile-user-agent')
            options.add_argument('--enable-touchview')
        if profile["browser"]["proxy"] is not None:
            options.add_argument(f'--proxy-server=socks5://' + profile["browser"]["proxy"])
            print('proxy= "' + profile["browser"]["proxy"] + '"')

        # additional options and capabilities from profile
        if len(profile["chromeoptions"]["arguments"]) > 0:
            for arg in profile["chromeoptions"]["arguments"]:
                options.add_argument(arg)
        if len(profile["chromeoptions"]["capabilities"]) > 0:
            for cap in profile["chromeoptions"]["capabilities"]:
                options.set_capability(cap[0], cap[1])

        # ModHeader extension options
        if not profile["plugins"]["modheader"] is False:
            if not profile["browser"]["inkognito"]:
                warnings.warn('Only use modheader when additional Headers needed!')
                options.add_argument('--load-extension=' + profile["plugins"]["modheader"])
            else:
                warnings.warn('Modheader not supported in Incognito!, disabling')

        # Actual start of chrome
        if not profile["plugins"]["modheader"] is False:  # for using ModHeader extension
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager

            self.driver = uc.Chrome(use_subprocess=True, options=options,
                                    service=Service(ChromeDriverManager().install()),
                                    keep_alive=True)  # start undetected_chromedriver
        else:  # ModHeader not needed
            self.driver = uc.Chrome(use_subprocess=True, options=options,
                                    keep_alive=True)  # start undetected_chromedriver

        self.driver.get('http://icanhazip.com/')  # wait browser to start

        # initial property
        self.driver.evaluate_on_document_identifiers = {}

        # functions to execute
        x = self.driver.execute_cdp_cmd('Emulation.setIdleOverride', {'isUserActive': True, 'isScreenUnlocked': True})
        self.set_touch(profile["device"]["touch_device"], maxpoints=profile["device"]["maxtouchpoints"])
        self.set_emulation(profile["device"]["emulation"], enabled=mobile)
        self.pointer_as_touch(mobile, profile["browser"]["pointer_as_touch"])
        self.set_darkmode(enabled=profile["browser"]["darkmode"], mobile=mobile)
        self.set_useragent(profile["device"]["agent_override"])
        self.get_navigator()

        # additional cdp_cmd commands from profile
        if len(profile["cdp_cmd"]) > 0:
            for args in profile["cdp_cmd"]:
                self.driver.execute_cdp_cmd(args[0], args[1])

        if not (profile["evaluate_on_new_document"] is None):
            print('identifier for ""evaluate_on_new_document" in profile is :' + str(
                self.evaluate_on_new_document(profile["evaluate_on_new_document"])))

        # set webdriver js var to false
        self.define_prop_on_new_document("navigator", "webdriver", False)
        # remove plugins when mobile
        if mobile:
            self.define_prop_on_new_document("navigator", "plugins", [])

        # add my functions to driver
        self.driver.set_touch = self.set_touch
        self.driver.set_emulation = self.set_emulation
        self.driver.pointer_as_touch = self.pointer_as_touch
        self.driver.set_darkmode = self.set_darkmode
        self.driver.set_set_useragent = self.set_useragent
        self.driver.get_profile = self.get_profile
        self.driver.get_navigator = self.get_navigator
        self.driver.send_keys = self.sendkeys
        self.driver.navigator2profile = navigator2profile
        self.driver.profile = profile
        self.driver.evaluate_on_new_document = self.evaluate_on_new_document
        self.driver.remove_evaluate_on_document = self.remove_evaluate_on_document
        self.driver.define_prop_on_new_document = self.define_prop_on_new_document

        # Return actual driver
        return self.driver

    def set_touch(self, enabled=True, maxpoints=5) -> (bool, int):  # set touch options
        return self.driver.execute_cdp_cmd('Emulation.setTouchEmulationEnabled',
                                           {'enabled': enabled, 'maxTouchPoints': maxpoints})  # already set in options

    # set emulation props, disabling not supported!
    def set_emulation(self, emulation, enabled=True) -> (Dict[str, int or Dict[str, str or int or float]], bool):
        emulation.update({"mobile": enabled})
        if enabled:
            warnings.warn('disabling emulation not supported')
            x = self.driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', emulation)
            return self.driver.execute_cdp_cmd('Page.setDeviceMetricsOverride', emulation), x

    # set pointer as touch (makes code hung)
    def pointer_as_touch(self, mobile, enabled=True) -> (bool, bool):
        if mobile:
            config = 'mobile'
        else:
            config = 'desktop'
        if enabled:
            warnings.warn('Actions execute, but then take long when "EmitTouchEventsForMouse"!')
        return self.driver.execute_cdp_cmd('Emulation.setEmitTouchEventsForMouse', {'enabled': enabled,
                                                                                    'configuration': config})  # executes, but then takes long [maybe check if success?]

    # set force darkmode
    def set_darkmode(self, enabled=True, mobile=True) -> (bool, bool):
        if not mobile:
            warnings.warn('darkmode might look weird without mobile_view!')
        else:
            return self.driver.execute_cdp_cmd('Emulation.setAutoDarkModeOverride',
                                               {'enabled': enabled})

    # set useragent
    def set_useragent(self, useragent) -> Dict[str, str or Dict[str, str or bool or List[Dict[str, str]]]]:
        x = self.driver.execute_cdp_cmd('Emulation.setUserAgentOverride', useragent)
        # noinspection PyTypeChecker
        return self.driver.execute_cdp_cmd("Network.setUserAgentOverride", useragent), x

    def start_no_profile(self):  # start minimal driver without profile
        options = uc.ChromeOptions()
        options.add_argument("--incognito")
        return uc.Chrome(use_subprocess=True, options=options, keep_alive=True)  # start undetected_chromedriver

    def evaluate_on_new_document(self, js: str):  # evaluate js on every new page
        identifier = int(
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})["identifier"])
        self.driver.evaluate_on_document_identifiers.update({identifier: js})
        return identifier

    # remove js evaluation  on every new page for specific script
    def remove_evaluate_on_document(self, identifier: int):
        del self.driver.evaluate_on_document_identifiers[identifier]
        return self.driver.execute_cdp_cmd("Page.removeScriptToEvaluateOnNewDocument", {"identifier": str(identifier)})

    # define var.property for javascript
    def define_prop_on_new_document(self, var, prop, val, func='get: ()') -> (str, str, any, str):
        self.evaluate_on_new_document(
            "Object.defineProperty(" + var + ", " + json.dumps(prop) + ", {" + func + " => " + json.dumps(val) + "})")

    # noinspection PyTypeChecker
    # get profile from current driver
    def get_profile(self, filename: str or None = None) -> str:
        navigator = self.get_navigator()
        return navigator2profile(navigator, filename=filename)

    # get "navigator", object convertible to profile with "navigator2profile"
    def get_navigator(self):
        # noinspection PyBroadException
        try:
            self.returnnavigator = self.driver.execute_script(self.js_return_navigator)
        except:
            traceback.print_exc()
            warnings.warn('get_navigator.js executed incorrectly!')
        return self.returnnavigator

    def sendkeys(self, keys):  # send keys without specific Element
        actions = ActionChains(self.driver)
        actions.send_keys(str(keys))
        actions.perform()


# convert exported "navigator" to Profile
def navigator2profile(navigator: dict, filename: str = None):
    from utils import write_json

    def replace_none(var, replace_with):
        if var is not None:
            return var
        else:
            return replace_with

    if navigator is not None:
        try:
            navigator["metrics"]["orientation"] = replace_none(navigator["metrics"]["orientation"], "portrait-primary")
            navigator["metrics"]["angle"] = replace_none(navigator["metrics"]["angle"], 0)

            empty_profile = {}
            # Map & convert Values to Profile
            empty_profile.update({'device': {'mobile': navigator["useragentdata"]["mobile"],
                                             'model': '',
                                             'language': navigator["language"],
                                             'touch_device': navigator["metrics"]["maxtouchpoints"] > 0,
                                             'maxtouchpoints': navigator["metrics"]["maxtouchpoints"],
                                             'hardware_accel': False,
                                             'emulation': {'width': navigator["metrics"]["width"],
                                                           'height': navigator["metrics"]["height"],
                                                           'deviceScaleFactor': navigator["metrics"]["scale_factor"],
                                                           'screenOrientation': {
                                                               'type': navigator["metrics"]["orientation"],
                                                               'angle': navigator["metrics"]["angle"]}},
                                             'agent_override': {'platform': navigator["platform"],
                                                                'userAgent': navigator["useragent"],
                                                                'userAgentMetadata': {
                                                                    'brands': navigator["useragentdata"]["brands"],
                                                                    'fullVersionList': navigator["useragentdata"][
                                                                        "brands"],
                                                                    'fullVersion':
                                                                        navigator["useragentdata"]["brands"][0][
                                                                            "version"] + '.0.0000.00',
                                                                    'platform': navigator["useragentdata"]["platform"],
                                                                    'platformVersion': '10.0.0', 'architecture': 'x86',
                                                                    'model': '',
                                                                    'mobile': navigator["useragentdata"]["mobile"],
                                                                    'bitness': '',
                                                                    'wow64': navigator["wow64"]}}},
                                  'browser': {'sandbox': True,
                                              'inkognito': True,
                                              'proxy': None,
                                              'darkmode': navigator["useragentdata"]["mobile"],
                                              'pointer_as_touch': False,
                                              'mobile_view': navigator["useragentdata"]["mobile"],
                                              'app': False,
                                              'touch_events': navigator["metrics"]["maxtouchpoints"] > 0,
                                              'window_size': {'x': navigator["metrics"]["width"],
                                                              'y': navigator["metrics"]["height"]}},
                                  'chromeoptions': {'arguments': [], 'capabilities': []},
                                  'cdp_cmd': [],
                                  'plugins': {'selenium-wire': False, 'modheader': False, 'stealth': False,
                                              "buster": False}})
        except:
            traceback.print_exc()
            raise ValueError("Navigator not converted correctly!")
        if not (filename is None):
            write_json(empty_profile, filename=filename)
        return empty_profile
    else:
        raise ValueError("navigator was None!")
