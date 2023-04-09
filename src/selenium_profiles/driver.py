import warnings
from collections import defaultdict

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

from selenium_profiles.scripts import profiles
from selenium_profiles.utils.colab_utils import is_colab
from selenium_profiles.scripts.cdp_tools import cdp_tools
from selenium_profiles.scripts import undetected
from selenium_profiles.scripts.driver_utils import requests, actions

from selenium_profiles.utils.utils import sel_profiles_path  # read txt files


# noinspection PyPep8Naming,GrazieInspection
class driver(object):
    def __init__(self):
        # initial attributes
        # noinspection SpellCheckingInspection
        self.returnnavigator = None
        self.profile = None
        self.driver = None
        self.cdp_tools = None
        self.options = None

        self.profiles = profiles.profiles()

    # noinspection PyUnresolvedReferences
    def start(self, profile: dict, uc_driver: bool = False, executable_path:str = None, chrome_binary:str=None):
        self.profile = defaultdict(lambda: None)
        self.profile.update(profile)

        if is_colab():  # google-colab doesn't support sandbox!
            # todo: nested default-dict with Lambda: None
            if "options" in self.profile.keys():
                if "browser" in self.profile["options"].keys():
                    if "sandbox" in self.profile["options"]["browser"].keys():
                        if self.profile["options"]["browser"]["sandbox"] is True:
                            warnings.warn('Google-colab doesn\'t work with sandbox enabled yet, disabling..')
                    else:
                        self.profile["options"]["browser"].update({"sandbox":False})
                else:
                    self.profile["options"].update({"browser":{"sandbox":False}})
            else:
                # noinspection PyTypeChecker
                self.profile.update({"options":{"browser":{"sandbox":False}}})

        if uc_driver:
            import undetected_chromedriver as uc  # undetected chromedriver
            self.options = uc.ChromeOptions()  # selenium.webdriver options, https://peter.sh/experiments/chromium-command-line-switches/
        else:
            self.options = webdriver.ChromeOptions()

        # options-manager
        self.options = self.profiles.options.set(options=self.options, options_profile=self.profile["options"])

        if executable_path is None: # chromedriver path
            if uc_driver:
                executable_path = None
            else:
                from selenium.webdriver.chrome.service import DEFAULT_EXECUTABLE_PATH
                executable_path = DEFAULT_EXECUTABLE_PATH

        service = ChromeService(executable_path=executable_path)


        if not (chrome_binary is None):
            self.options.binary_location = chrome_binary

        # ACTUAL START

        if uc_driver:
            # noinspection PyUnboundLocalVariable
            self.driver = uc.Chrome(use_subprocess=True, options=self.options, keep_alive=True, driver_executable_path=executable_path)  # start undetected_chromedriver
        else:
            try:
                # noinspection PyUnresolvedReferences
                adb = self.profile["options"]["adb"]
            except TypeError:
                adb = None
            except KeyError:
                adb = None

            self.options = undetected.config_options(self.options, adb=adb)

            # Actual start of chrome
            self.driver = webdriver.Chrome(options=self.options, service=service)  # start selenium webdriver

        self.driver.get("http://lumtest.com/myip.json")  # wait browser to start

        self.cdp_tools = cdp_tools(self.driver)

        self.cdp_tools.evaluate_on_document_identifiers.update({1: # we know that it is there:)
                """(function () {window.cdc_adoQpoasnfa76pfcZLmcfl_Array = window.Array;
                window.cdc_adoQpoasnfa76pfcZLmcfl_Object = window.Object;
                window.cdc_adoQpoasnfa76pfcZLmcfl_Promise = window.Promise;
                window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy = window.Proxy;
                window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol = window.Symbol;
                }) ();"""})

        # execute cdp based on profile
        self.profiles.cdp.set(driver=self.driver, cdp_profile=self.profile["cdp"])

        if not uc_driver:
            undetected.exec_cdp(self.driver, self.cdp_tools)

        self.driver.profile = self.profile
        self.driver.options = self.options
        self.add_funcs_to_driver()

        # Return actual driver
        return self.driver

    def add_funcs_to_driver(self):

        self.driver.cdp_tools = self.cdp_tools

        # add selenium-interceptor
        from selenium_interceptor.interceptor import cdp_listener
        self.driver.cdp_listener = cdp_listener(driver=self.driver)

        # add my functions to driver

        self.driver.get_profile = self.get_profile
        self.driver.requests = requests(self.driver)
        self.driver.actions = actions(self.driver)

        # patch cookie functions
        self.driver.get_cookies = self.cdp_tools.get_cookies
        self.driver.add_cookie = self.cdp_tools.add_cookie
        self.driver.get_cookie = self.cdp_tools.get_cookie
        self.driver.delete_cookie = self.cdp_tools.delete_cookie
        self.driver.delete_all_cookies = self.cdp_tools.delete_all_cookies

    def export_profile(self, to_path=sel_profiles_path() + "files/user_dir"):
        import shutil
        shutil.copytree(self.driver.user_data_dir, to_path)

    def get_profile(self):
        from selenium_profiles.utils.utils import read
        js = read('js/export_profile.js')
        return self.driver.execute_async_script(js)
