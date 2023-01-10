import time  # for time.sleep()
import traceback  # print exception
import urllib  # for url parsing
import warnings
from collections import defaultdict

from selenium import webdriver
from selenium_profiles.scripts import profiles
from selenium_profiles.utils.colab_utils import is_colab
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

        self.profiles = profiles.profiles()

    def start(self, profile: dict, uc_driver: bool = False):
        self.profile = defaultdict(lambda: None)
        self.profile.update(profile)

        #if self.profile["plugins"]["selenium-wire"]:
        #    warnings.warn("Selenium-wire not supported yet, ignoring")

        if is_colab():  # google-colab doesn't support sandbox!
            if self.profile["options"]:
                # noinspection PyUnresolvedReferences
                if self.profile["options"]["sandbox"] is True:
                    warnings.warn('Google-colab doesn\'t work with sandbox enabled yet, disabling..')
            else:
                # noinspection PyTypeChecker
                self.profile["options"] = {}
            # noinspection PyUnresolvedReferences
            self.profile["options"].update({"sandbox":True})

        if uc_driver:
            try:
                # noinspection PyUnresolvedReferences
                import undetected_chromedriver as uc  # undetected chromedriver
            except ImportError:
                warnings.warn('undetected-chromedriver not installed. Installing..')
                import os
                from selenium_profiles.utils.colab_utils import patch_uc
                os.system('pip install undetected-chromedriver')
                patch_uc()
            # noinspection PyUnboundLocalVariable
            self.options = uc.ChromeOptions()  # selenium.webdriver options, https://peter.sh/experiments/chromium-command-line-switches/
        else:
            self.options = webdriver.ChromeOptions()  # selenium.webdriver options, https://peter.sh/experiments/chromium-command-line-switches/

        # options-manager
        self.options = self.profiles.options.set(options=self.options, options_profile=self.profile["options"])

        # EXTENSIONS

        # # Buster
        # if self.profile["plugins"]["buster"]:
        #     import os
        #     warnings.warn("Buster is deprecated and automating isn't supported!")
        #     warnings.warn('Only use Buster when Captcha solver needed!')
        #     if not os.path.isdir(sel_profiles_path() + "files/buster"):
        #         warnings.warn('Buster not installed & extracted in /buster yet!')
        #         from selenium_profiles.utils.installer import install_buster
        #         install_buster()
        #     self.options.add_argument('--load-extension=' + sel_profiles_path() + "files/buster")

        # ACTUAL START

        if uc_driver:
            # noinspection PyUnboundLocalVariable
            self.driver = uc.Chrome(use_subprocess=True, options=self.options, keep_alive=True,
                                    browser_executable_path=find_chrome_executable())  # start undetected_chromedriver
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
            self.driver = webdriver.Chrome(options=self.options)  # start selenium webdriver

        self.driver.get('http://motherfuckingwebsite.com/')  # wait browser to start

        self.cdp_tools = cdp_tools(self.driver)

        self.cdp_tools.delete_all_cookies()  # delete website cookies

        # execute cdp based on profile
        self.profiles.cdp.set(driver=self.driver, cdp_profile=self.profile["cdp"])

        profiles.exec_js_evaluators(self.profile, self.driver, self.cdp_tools)

        if not uc_driver:
            undetected.exec_cdp(self.driver, self.cdp_tools)

        self.driver.profile = self.profile
        self.driver.options = self.options
        self.add_funcs_to_driver()

        # Return actual driver
        return self.driver

    def add_funcs_to_driver(self):

        self.driver.cdp_tools = self.cdp_tools

        # add my functions to driver
        self.driver.send_keys = sendkeys
        self.driver.get_profile =self.get_profile

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

    def get_profile(self):
        from selenium_profiles.utils.utils import read
        js = read('js/get_navigator.js')
        # noinspection PyBroadException
        self.driver.execute_script(js)
        time.sleep(1)
        return self.driver.execute_script('return window.useragent')

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
