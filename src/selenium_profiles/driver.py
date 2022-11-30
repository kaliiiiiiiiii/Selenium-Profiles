import time  # for time.sleep()
import traceback  # print exception
import urllib  # for url parsing
import warnings
from typing import Dict  # define types in functions

import undetected_chromedriver as uc  # undetected chromedriver
from selenium import webdriver
from selenium_profiles.scripts import profiles
from selenium_profiles.scripts.cdp_tools import cdp_tools
from selenium_profiles.scripts.driver_utils import sendkeys
from selenium_profiles.scripts import undetected
from selenium_profiles.utils.utils import sel_profiles_path, find_chrome_executable  # read txt files


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

        self.profiles = profiles

    def start(self, profile: Dict[str, dict or list], uc_driver: bool = False):
        self.profile = profile

        if not self.profile["plugins"]["selenium-wire"] is False:
            warnings.warn("Selenium-wire not supported yet, ignoring")

        if uc_driver:
            self.options = uc.ChromeOptions()  # selenium.webdriver options, https://peter.sh/experiments/chromium-command-line-switches/
        else:
            self.options = webdriver.ChromeOptions()  # selenium.webdriver options, https://peter.sh/experiments/chromium-command-line-switches/

        # options-manager
        self.options = self.profiles.to_options(self.profile, self.options)

        # EXTENSIONS

        # ModHeader
        if not (self.profile["plugins"]["modheader"] is False):
            import os
            warnings.warn('Only use modheader when additional Headers needed!')
            if not os.path.isdir(sel_profiles_path() + "files/modheader"):
                warnings.warn('Modheader not installed & extracted in /modheader yet!')
                from selenium_profiles.utils.installer import install_modheader
                install_modheader()
            self.options.add_argument('--load-extension=' + sel_profiles_path() + "files/modheader")

        # Buster
        if not self.profile["plugins"]["buster"] is False:
            import os
            warnings.warn("Buster is deprecated and automating isn't supported!")
            warnings.warn('Only use Buster when Captcha solver needed!')
            if not os.path.isdir(sel_profiles_path() + "files/buster"):
                warnings.warn('Buster not installed & extracted in /buster yet!')
                from selenium_profiles.utils.installer import install_buster
                install_buster()
            self.options.add_argument('--load-extension=' + sel_profiles_path() + "files/buster")

        # ACTUAL START

        if uc_driver:
            self.driver = uc.Chrome(use_subprocess=True, options=self.options, keep_alive=True,
                                    browser_executable_path=find_chrome_executable())  # start undetected_chromedriver
        else:
            self.options = undetected.config_options(self.options)

            # Actual start of chrome
            self.driver = webdriver.Chrome(options=self.options)  # start selenium webdriver

        self.driver.get('http://motherfuckingwebsite.com/')  # wait browser to start

        self.cdp_tools = cdp_tools(self.driver)

        # execute cdp based on profile
        self.profiles.exec_cdp(self.profile, self.driver)

        self.profiles.exec_js_evaluators(self.profile, self.driver, self.cdp_tools)

        if not uc_driver:
            undetected.exec_cdp(self.driver, self.cdp_tools)

        if not (profile["plugins"]["modheader"] is False):
            self.load_header_profiles(profile["plugins"]["modheader"])

        self.driver.profile = profile
        self.add_funcs_to_driver()

        # Return actual driver
        return self.driver

    def add_funcs_to_driver(self):

        self.driver.cdp_tools = self.cdp_tools

        # add my functions to driver
        self.driver.send_keys = sendkeys

        self.driver.get_profile = self.profiles.get_profile
        self.driver.get_navigator = self.profiles.get_navigator
        self.driver.navigator2profile = profiles.navigator2profile

        # ModHeader
        self.driver.load_header_profiles = self.load_header_profiles
        self.driver.clear_headers = self.clear_headers

        # Captcha
        self.driver.solve_captcha = self.solve_captcha

        # patch cookie functions
        self.driver.get_cookies = self.cdp_tools.get_cookies
        self.driver.add_cookie = self.cdp_tools.add_cookie
        self.driver.get_cookie = self.cdp_tools.get_cookie
        self.driver.delete_cookie = self.cdp_tools.delete_cookie
        self.driver.delete_all_cookies = self.cdp_tools.delete_all_cookies

    def export_profile(self, to_path=sel_profiles_path() + "files/user_dir"):
        import shutil
        shutil.copytree(self.driver.user_data_dir, to_path)

    def start_no_profile(self, modheader: bool = False, buster: bool = False, user_dir: str = None,
                         arguments: list = []):  # start minimal driver without profile
        options = uc.ChromeOptions()
        # additional options
        if len(arguments) > 0:
            for arg in arguments:
                options.add_argument(arg)

        options.arguments.extend(["--no-sandbox", "--test-type"])

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

        self.driver = uc.Chrome(use_subprocess=True, options=options, keep_alive=True,
                                browser_executable_path=find_chrome_executable())  # start undetected_chromedriver

        self.add_funcs_to_driver()

        return self.driver

    # noinspection PyUnresolvedReferences
    def load_header_profiles(self, profile: str):
        if not self.profile["plugins"]["modheader"] is False:
            self.driver.modheader_url = 'https://webdriver.modheader.com/load?profile=' + urllib.parse.quote(
                profile[1:-1], safe='')
            self.driver.get(
                'https://webdriver.modheader.com/load?profile=' + urllib.parse.quote(profile[1:-1], safe=''))
        else:
            warnings.warn('ModHeader needs to be enabled for custom headers!')

    def clear_headers(self):
        if self.profile["plugins"]["modheader"] is not False:
            self.driver.get('https://webdriver.modheader.com/clear')
        else:
            warnings.warn('ModHeader needs to be enabled for custom headers!')

    def solve_captcha(self):
        from selenium.webdriver.common.by import By  # locate elements
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait

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
