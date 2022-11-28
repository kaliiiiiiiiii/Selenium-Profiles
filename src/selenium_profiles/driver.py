import warnings
import undetected_chromedriver as uc  # undetected chromedriver
from selenium.webdriver.common.action_chains import ActionChains  # Type text without specific Element
from selenium_profiles.utils.utils import read, sel_profiles_path, find_chrome_executable  # read txt files
import traceback  # print exception
from typing import Dict, List  # define types in functions
import json  # python dict to js
import urllib  # for url parsing
import time  # for time.sleep()
from selenium_profiles.utils.colab_utils import is_collab, display


# noinspection PyShadowingNames
def sendkeys(driver, keys):  # send keys without specific Element
    actions = ActionChains(driver)
    actions.send_keys(str(keys))
    actions.perform()


# noinspection PyPep8Naming,GrazieInspection
class driver(object):
    def __init__(self):
        # initial attributes
        self.overwride_quit = None
        self.returnnavigator = None
        self.profile = None
        self.driver = None
        self.js_return_navigator = read('js/get_navigator.js')[0]  # for exporting javascript Variables

    def start(self, profile: Dict[str, dict or list]):
        self.profile = profile
        mobile = profile['device']['mobile']

        if not profile["plugins"]["selenium-wire"] is False:
            warnings.warn("Selenium-wire not supported yet, ignoring")

        options = uc.ChromeOptions()  # selenium.webdriver options, https://peter.sh/experiments/chromium-command-line-switches/

        # always used options
        size = profile["browser"]["window_size"]
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
            options.add_argument('--headless=chrome')
            options.add_argument("--blink-settings=imagesEnabled=false")  # disable loading Images
        if profile["browser"]["touch_events"]:
            options.add_argument("--touch-events=enabled")
        if profile["browser"]["app"]:
            options.add_argument('--app')
            options.add_argument('--force-app-mode')
        if profile["device"]["touch_device"]:
            options.add_argument("--touch-events=enabled")  # enable touch events
        if profile["browser"]["inkognito"]:
            if (profile["plugins"]["modheader"] is False) and (profile["plugins"]["buster"] is False):
                options.add_argument("--incognito")
            else:
                warnings.warn('Incognito not working with Extensions!, disabling Incognito')
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
            options.add_argument('--proxy-server=socks5://' + profile["browser"]["proxy"])
            print('proxy= "' + profile["browser"]["proxy"] + '"')

        # additional options and capabilities from profile
        if len(profile["chromeoptions"]["arguments"]) > 0:
            for arg in profile["chromeoptions"]["arguments"]:
                options.add_argument(arg)
        if len(profile["chromeoptions"]["capabilities"][0]) > 0:
            for cap in profile["chromeoptions"]["capabilities"]:
                options.set_capability(cap[0], cap[1])

        # ModHeader extension options
        if not (profile["plugins"]["modheader"] is False):
            import os
            warnings.warn('Only use modheader when additional Headers needed!')
            if not os.path.isdir(sel_profiles_path() + "files/modheader"):
                warnings.warn('Modheader not installed & extracted in /modheader yet!')
                from selenium_profiles.utils.installer import install_modheader
                install_modheader()
            options.add_argument('--load-extension=' + sel_profiles_path() + "files/modheader")

        # Buster extension options
        if not profile["plugins"]["buster"] is False:
            import os
            warnings.warn("Buster is deprecated and automating isn't supported!")
            warnings.warn('Only use Buster when Captcha solver needed!')
            if not os.path.isdir(sel_profiles_path() + "files/buster"):
                warnings.warn('Buster not installed & extracted in /buster yet!')
                from selenium_profiles.utils.installer import install_buster
                install_buster()
            options.add_argument('--load-extension=' + sel_profiles_path() + "files/buster")

        if is_collab():
            display.start_display()  # todo: stop display missing!

        # Actual start of chrome
        self.driver = uc.Chrome(use_subprocess=True, options=options, keep_alive=True, browser_executable_path=find_chrome_executable())  # start undetected_chromedriver

        self.driver.get('http://icanhazip.com/')  # wait browser to start

        # initial property
        self.driver.evaluate_on_document_identifiers = {}

        # functions to execute
        # noinspection PyUnusedLocal
        x = self.driver.execute_cdp_cmd('Emulation.setIdleOverride', {'isUserActive': True, 'isScreenUnlocked': True})
        self.set_touch(profile["device"]["touch_device"], maxpoints=profile["device"]["maxtouchpoints"])
        self.set_emulation(profile["device"]["emulation"], enabled=mobile)
        self.pointer_as_touch(mobile, profile["browser"]["pointer_as_touch"])
        self.set_darkmode(enabled=profile["browser"]["darkmode"], mobile=mobile)
        self.set_useragent(profile["device"]["agent_override"])
        self.get_navigator()
        self.driver.headers = []

        if not (profile["plugins"]["modheader"] is False):
            self.load_header_profiles(profile["plugins"]["modheader"])

        # additional cdp_cmd commands from profile
        if len(profile["cdp_cmd"][0]) > 0:
            for args in profile["cdp_cmd"]:
                self.driver.execute_cdp_cmd(args[0], args[1])

        # additional evaluate on new document
        if not (profile["evaluate_on_new_document"] is None):
            print('identifier for ""evaluate_on_new_document" in profile is :' + str(
                self.evaluate_on_new_document(profile["evaluate_on_new_document"])))

        # set webdriver js var to false
        self.define_prop_on_new_document("navigator", "webdriver", False)
        # remove plugins when mobile
        if mobile:
            self.define_prop_on_new_document("navigator", "plugins", [])

        self.driver.profile = profile
        self.add_my_functions()

        # Return actual driver
        return self.driver

    def add_my_functions(self):
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
        self.driver.evaluate_on_new_document = self.evaluate_on_new_document
        self.driver.remove_evaluate_on_document = self.remove_evaluate_on_document
        self.driver.define_prop_on_new_document = self.define_prop_on_new_document
        self.driver.load_header_profiles = self.load_header_profiles
        self.driver.clear_header = self.clear_header
        self.driver.solve_captcha = self.solve_captcha
        self.driver.get_cookies = self.get_cookies
        self.driver.add_cookie = self.add_cookie
        self.driver.get_cookie = self.get_cookie
        self.driver.delete_cookie = self.delete_cookie
        self.driver.delete_all_cookies = self.delete_all_cookies

    def export_profile(self, to_path=sel_profiles_path() + "files/user_dir"):
        import shutil
        shutil.copytree(self.driver.user_data_dir, to_path)

    def set_touch(self, enabled=True, maxpoints=5) -> (bool, int):  # set touch options
        return self.driver.execute_cdp_cmd('Emulation.setTouchEmulationEnabled',
                                           {'enabled': enabled, 'maxTouchPoints': maxpoints})  # already set in options

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
        if not mobile and enabled:
            warnings.warn('darkmode might look weird without mobile_view!')
        else:
            return self.driver.execute_cdp_cmd('Emulation.setAutoDarkModeOverride',
                                               {'enabled': enabled})

    # set useragent
    def set_useragent(self, useragent) -> Dict[str, str or Dict[str, str or bool or List[Dict[str, str]]]]:
        x = self.driver.execute_cdp_cmd('Emulation.setUserAgentOverride', useragent)
        # noinspection PyTypeChecker
        return self.driver.execute_cdp_cmd("Network.setUserAgentOverride", useragent), x

    def start_no_profile(self, modheader: bool = False, buster: bool = False, user_dir: str = None,
                         arguments: list = []):  # start minimal driver without profile
        options = uc.ChromeOptions()
        # additional options
        if len(arguments) > 0:
            for arg in arguments:
                options.add_argument(arg)

        options.add_argument("--no-sandbox")

        if not (user_dir is None):
            options.add_argument(r"--user-data-dir=" + user_dir)

        # ModHeader extension options
        if modheader:
            import os
            warnings.warn('Only use modheader when additional Headers needed!')
            if not os.path.isdir(os.getcwd() + "/modheader"):
                warnings.warn('Modheader not installed & extracted in /modheader yet!')
                from selenium_profiles.utils.installer import install_modheader
                install_modheader()
            options.add_argument('--load-extension=' + os.getcwd() + "/modheader")

        # Buster extension options
        if buster:
            import os
            warnings.warn("Buster is deprecated and automating isn't supported!")
            warnings.warn('Only use Buster when Captcha solver needed!')
            if not os.path.isdir(os.getcwd() + "/buster"):
                warnings.warn('Buster not installed & extracted in /buster yet!')
                from selenium_profiles.utils.installer import install_buster
                install_buster()
            options.add_argument('--load-extension=' + os.getcwd() + "/buster")

        self.driver = uc.Chrome(use_subprocess=True, options=options, keep_alive=True, browser_executable_path=find_chrome_executable())  # start undetected_chromedriver

        self.add_my_functions()

        return self.driver

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

    # noinspection PyUnresolvedReferences
    def load_header_profiles(self, profile: str):
        if not self.profile["plugins"]["modheader"] is False:
            self.driver.modheader_url = 'https://webdriver.modheader.com/load?profile=' + urllib.parse.quote(
                profile[1:-1], safe='')
            self.driver.get(
                'https://webdriver.modheader.com/load?profile=' + urllib.parse.quote(profile[1:-1], safe=''))
        else:
            warnings.warn('ModHeader needs to be enabled for custom headers!')

    def clear_header(self):
        if self.profile["plugins"]["modheader"] is not False:
            self.driver.get('https://webdriver.modheader.com/clear')
            self.driver.headers = []
        else:
            warnings.warn('ModHeader needs to be enabled for custom headers!')

    def solve_captcha(self):
        from selenium.webdriver.common.by import By  # locate elements
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait

        solve_script = read("js/solve_script.js")
        # noinspection PyBroadException
        try:
            wait = WebDriverWait(self.driver, 5)  # driver 5s timeout
            #  click on captcha
            wait.until(EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
            wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
            self.driver.switch_to.default_content()
            # click on audio
            WebDriverWait(self.driver, 4).until(EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[name^='c-'][src^='https://www.google.com/recaptcha/api2/bframe?']")))
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="recaptcha-audio-button"]').click()
            self.driver.switch_to.default_content()
        except:
            # check "try again later"
            WebDriverWait(self.driver, 4).until(EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[name^='c-'][src^='https://www.google.com/recaptcha/api2/bframe?']")))
            self.driver.find_element(By.CSS_SELECTOR,
                                     "a[href='https://developers.google.com/recaptcha/docs/faq#my-computer-or-network-may-be-sending-automated-queries']")
            traceback.print_exc()
            warnings.warn("Captcha could not be solved!")
            self.driver.switch_to.default_content()

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
def navigator2profile(navigator, filename=None) -> (dict or str, str):
    from selenium_profiles.utils.utils import write_json

    def replace_none(var, replace_with):
        if var is not None:
            return var
        else:
            return replace_with

    if navigator is not None:
        if type(navigator) is str:
            navigator = json.loads(navigator)
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
