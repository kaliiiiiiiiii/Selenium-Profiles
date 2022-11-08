import warnings
import undetected_chromedriver as uc  # undetected chromedriver
from selenium.webdriver.common.action_chains import ActionChains  # Type text without specific Element
from utils import read  # read txt files
import traceback  # print exception
from typing import Dict, List


class driver:
    def __init__(self):
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

        size = profile["browser"]["window_size"]
        options.add_argument("--window-size=" + str(size["x"]) + "," + str(size["y"]))
        options.add_argument('--user-agent=' + profile["device"]["agent_override"]["userAgent"])
        options.set_capability("platformName", profile["device"]["agent_override"]["userAgentMetadata"][
            "platform"])  # todo does it have an effect?

        if not profile["browser"]["sandbox"]:
            options.add_argument('--no-sandbox ')
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

        if len(profile["chromeoptions"]["arguments"]) > 0:
            for arg in profile["chromeoptions"]["arguments"]:
                options.add_argument(arg)
        if len(profile["chromeoptions"]["capabilities"]) > 0:
            for cap in profile["chromeoptions"]["capabilities"]:
                options.set_capability(cap)

        if not profile["plugins"]["modheader"] is False:
            if not profile["browser"]["inkognito"]:
                warnings.warn('Only use modheader when additional Headers needed!')
                options.add_argument('--load-extension=' + profile["plugins"]["modheader"])
            else:
                warnings.warn('Modheader not supported in Incognito!, disabling')

        ## Actual start of chrome
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

        if len(profile["cdp_cmd"]) > 0:
            for args in profile["cdp_cmd"]:
                self.driver.execute_cdp_cmd(args[0], args[1])

        x = self.driver.execute_cdp_cmd('Emulation.setIdleOverride', {'isUserActive': True, 'isScreenUnlocked': True})
        self.set_touch(profile["device"]["touch_device"], maxpoints=profile["device"]["maxtouchpoints"])
        self.set_emulation(profile["device"]["emulation"], enabled=mobile)
        self.pointer_as_touch(mobile, profile["browser"]["pointer_as_touch"])
        self.set_darkmode(enabled=profile["browser"]["darkmode"], mobile=mobile)
        self.set_useragent(profile["device"]["agent_override"])

        if len(profile["cdp_cmd"]) > 0:
            for cmd in profile["cdp_cmd"]:
                self.driver.execute_cdp_cmd(cmd[0], cmd[1])

        # Return actual driver
        return self.driver

    def set_touch(self, enabled=True, maxpoints=5) -> (bool, int):
        return self.driver.execute_cdp_cmd('Emulation.setTouchEmulationEnabled',
                                           {'enabled': enabled, 'maxTouchPoints': maxpoints})  # already set in options

    def set_emulation(self, emulation, enabled=True) -> (Dict[str, int or Dict[str, str or int or float]], bool):
        emulation.update({"mobile": enabled})
        if enabled:
            warnings.warn('disabling emulation not supported')
            x = self.driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', emulation)
            return self.driver.execute_cdp_cmd('Page.setDeviceMetricsOverride', emulation), x

    def pointer_as_touch(self, mobile, enabled=True) -> (bool, bool):
        if mobile:
            config = 'mobile'
        else:
            config = 'desktop'
        if enabled:
            warnings.warn('Actions execute, but then take long when "EmitTouchEventsForMouse"!')
        return self.driver.execute_cdp_cmd('Emulation.setEmitTouchEventsForMouse', {'enabled': enabled,
                                                                                    'configuration': config})  # executes, but then takes long [maybe check if success?]

    def set_darkmode(self, enabled=True, mobile=True) -> (bool, bool):
        if not mobile:
            warnings.warn('darkmode might look weird without mobile_view!')
        else:
            return self.driver.execute_cdp_cmd('Emulation.setAutoDarkModeOverride',
                                               {'enabled': enabled})

    def set_useragent(self, useragent) -> Dict[str, str or Dict[str, str or bool or List[Dict[str, str]]]]:
        x = self.driver.execute_cdp_cmd('Emulation.setUserAgentOverride', useragent)
        return self.driver.execute_cdp_cmd("Network.setUserAgentOverride", useragent), x

    def start_no_profile(self):
        options = uc.ChromeOptions()
        options.add_argument("--incognito")
        return uc.Chrome(use_subprocess=True, options=options, keep_alive=True)  # start undetected_chromedriver

    def get_profile(self, filename=None) -> str:
        navigator = self.get_navigator()
        return navigator2profile(navigator, filename=filename)

    def get_navigator(self):
        try:
            self.returnnavigator = self.driver.execute_script(self.js_return_navigator)
        except:
            traceback.print_exc()
            warnings.warn('get_navigator.js executed incorrectly!')
        return self.returnnavigator


def sendkeys(driver, keys):  # send keys without specific Element
    actions = ActionChains(driver)
    actions.send_keys(str(keys))
    actions.perform()


# exported "navigator" to Profile
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
