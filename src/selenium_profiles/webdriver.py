import warnings
from collections import defaultdict
import typing

from selenium.webdriver.chrome.service import Service as ChromeService

from selenium_profiles.utils.colab_utils import is_colab
from selenium_profiles.scripts.profiles import options as options_handler

from selenium.webdriver import Chrome as BaseDriver
class Chrome(BaseDriver):

    # noinspection PyDefaultArgument
    def __init__(self, profile: dict = None, chrome_binary: str = None, executable_path: str = None,
                 options=None, duplicate_policy: str = "warn-add", safe_duplicates: list = list(),
                 base_drivers:tuple=None,
                 uc_driver: bool or None = None, seleniumwire_options: dict or bool or None = None,
                 injector_options:dict or bool or None = None, driverless_options = None,
                 **kwargs):


        import undetected_chromedriver as uc_webdriver
        if seleniumwire_options:
            import seleniumwire.undetected_chromedriver as wire_uc_webdriver
            from seleniumwire import webdriver as wire_webdriver


        from selenium_profiles.utils.utils import valid_key

        if not base_drivers:
            base_drivers = tuple()

        # import webdriver
        webdriver = None
        if uc_driver:
            if seleniumwire_options:
                # noinspection PyUnboundLocalVariable
                webdriver = wire_uc_webdriver
            else:
                webdriver = uc_webdriver
        else:
            if seleniumwire_options:
                # noinspection PyUnboundLocalVariable
                webdriver = wire_webdriver

        if webdriver:
            base_drivers = (webdriver.Chrome,) + base_drivers

        if not options:
            if webdriver:
                options = webdriver.ChromeOptions()
            else:
                from selenium.webdriver import ChromeOptions
                options = ChromeOptions()

        if driverless_options:
            try:
                # noinspection PyUnresolvedReferences
                from selenium_driverless.sync.webdriver import Chrome as DriverlessChrome
            except:
                raise RuntimeError("selenium-driverless requires Python>=3.8")
            base_drivers = base_drivers + (DriverlessChrome,)

        if len(base_drivers) > 1:
            warnings.warn("More than one base_driver might not initialize correctly, seems buggy.\n Also, you might try different order")
        if (len(base_drivers) == 1) and (base_drivers[0] == Chrome.__base__):
            pass # got selenium.webdriver.Chrome as BaseDriver
        elif not base_drivers:
            pass
        else :
            Chrome.__bases__ = base_drivers

        if not profile:
            profile = {}

        valid_key(profile.keys(), ["cdp", "options", "proxy"], "profile (selenium-profiles)")

        if type(seleniumwire_options) is dict:
            kwargs.update({"seleniumwire_options": seleniumwire_options})
        elif not (type(seleniumwire_options) is bool or seleniumwire_options is None):
            raise ValueError("Expected NoneType, dict or bool")

        defdict = defaultdict(lambda: None)
        defdict.update(profile)
        profile = defdict
        proxy = defaultdict(lambda :None)
        # noinspection PyTypeChecker
        if profile["proxy"]:
            # noinspection PyTypeChecker
            proxy.update(profile["proxy"])

        if proxy["proxy"] and (not seleniumwire_options):
            injector_options = True

        # sandbox handling for google-colab
        if is_colab():
            # todo: nested default-dict with Lambda: None
            if profile["options"]:
                # noinspection PyUnresolvedReferences
                if 'sandbox' in profile["options"].keys():
                    # noinspection PyUnresolvedReferences
                    if profile["options"]["sandbox"] is True:
                        warnings.warn('Google-colab doesn\'t work with sandbox enabled yet, disabling sandbox')
                else:
                    # noinspection PyUnresolvedReferences
                    profile["options"].update({"sandbox": False})
            else:
                # noinspection PyTypeChecker
                profile.update({"options": {"sandbox": False}})

        # options-manager
        options_manager = options_handler(options, profile["options"], duplicate_policy=duplicate_policy,
                                          safe_duplicates=safe_duplicates)

        # chrome executable path
        if chrome_binary:
            options_manager.Options.binary_location = chrome_binary

        if (uc_webdriver.Chrome in base_drivers) or (wire_uc_webdriver.Chrome in base_drivers):
            if executable_path:
                kwargs.update({"driver_executable_path": executable_path})
        elif driverless_options:
            pass
        else:
            # detectability options
            from selenium_profiles.scripts import undetected

            # is adb used ?
            try:
                # noinspection PyUnresolvedReferences
                adb = profile["options"]["adb"]
            except TypeError:
                adb = None
            except KeyError:
                adb = None

            options_manager.Options = undetected.config_options(options_manager.Options, adb=adb)

            # chromedriver path
            if executable_path:
                kwargs.update({"service": ChromeService(executable_path=executable_path)})

        injector = None
        if injector_options:
            from selenium_injector.scripts.injector import Injector
            if (injector_options is True) or injector_options == {}:
                injector_options = {}
            injector = Injector(**injector_options)
            options_manager.add_extensions(injector.paths)


        # add options to kwargs
        # noinspection PyProtectedMember,PyUnresolvedReferences
        options_manager.add_argument(f'--load-extension={",".join(options_manager._extensions)}')
        kwargs.update({"options": options_manager.Options})

        # Actual start of chrome
        super().__init__(**kwargs)
        # cdp tools

        self.get("chrome://version/")  # wait browser to start

        self.profiles = profiles(self, profile, selenium_injector=injector)


        self.profiles.cdp_handler.evaluate_on_document_identifiers.update({1:  # we know that it is there:)
                                                                """(function () {window.cdc_adoQpoasnfa76pfcZLmcfl_Array = window.Array;
                                                                window.cdc_adoQpoasnfa76pfcZLmcfl_Object = window.Object;
                                                                window.cdc_adoQpoasnfa76pfcZLmcfl_Promise = window.Promise;
                                                                window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy = window.Proxy;
                                                                window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol = window.Symbol;
                                                                }) ();"""})

        self.profiles.cdp_handler.apply(cdp_profile=profile["cdp"])

        if not (uc_driver or driverless_options):
            from selenium_profiles.scripts import undetected
            undetected.exec_cdp(self, cdp_handler=self.profiles.cdp_handler)

        if proxy["proxy"]:
            from selenium_profiles.utils.utils import valid_key
            # noinspection PyUnresolvedReferences
            valid_key(proxy.keys(), ["proxy", "bypass_list"], '"profiles["proxy"]"')
            # noinspection PyUnresolvedReferences
            self.profiles.proxy.set_single(proxy["proxy"], bypass_list=proxy["bypass_list"])

    def get_cookies(self, urls:typing.List[str] = None) -> typing.List[dict]:
        arg = {}
        if urls:
            arg["urls"] = urls
        return self.execute_cdp_cmd("Network.getAllCookies", arg)['cookies']

    def add_cookie(self, cookie_dict:dict) -> None:
        self.execute_cdp_cmd("Network.setCookie",cookie_dict)

    def delete_cookie(self, name:str, url:str=None, domain:str=None, path:str=None) -> None:
        arg = {"name": name}
        if url:
            arg["url"] = url
        if domain:
            arg["domain"] = domain
        if path:
            arg["path"] = path
        self.execute_cdp_cmd("Network.deleteCookies", arg)

    def delete_all_cookies(self) -> None:
        self.execute_cdp_cmd("Network.clearBrowserCookies", {})

    def quit(self) -> None:
        if "profiles" in self.__dir__():
            if "driverless" in self.profiles.__dir__():
                # noinspection PyUnresolvedReferences
                self.profiles.driverless.stop()
        super().quit()

class profiles:
    # noinspection PyShadowingNames
    def __init__(self, driver, profile, cdp_handler=None, selenium_injector=None):

        from selenium_interceptor.interceptor import cdp_listener
        from selenium_profiles.scripts.driver_utils import requests, actions
        from selenium_profiles.scripts.proxy import DynamicProxy

        self._driver = driver
        self._profile = profile
        self.injector = selenium_injector

        if cdp_handler:
            self.cdp_handler = cdp_handler
        elif "profiles" in driver.__dir__():
            self.cdp_handler = driver.profiles.cdp_handler
        else:
            from selenium_profiles.scripts.profiles import cdp_handler
            self.cdp_handler = cdp_handler(self._driver)

        self.cdp_listener = cdp_listener(driver=self._driver)
        self.actions = actions(self._driver)

        requests = requests(self._driver)
        self.fetch = requests.fetch
        try:
            self.proxy = DynamicProxy(self._driver, injector=self.injector)
        except ModuleNotFoundError:
            pass # not supported


    # noinspection PyShadowingNames
    def apply(self, profile: dict):
        """
        apply options after driver already started
        :param profile: selenium-profiles options
        """
        from selenium_profiles.utils.utils import valid_key
        valid_key(profile.keys(), ["cdp", "options"], "profile (selenium-profiles)")
        if "options" in profile.keys():
            warnings.warn('profile["options"] can\'t be applied when driver already started')
        if "cdp" in profile.keys():
            # noinspection PyUnresolvedReferences
            self.cdp_handler.apply(profile["cdp"])

    def get_profile(self):
        from selenium_profiles.utils.utils import read
        js = read('js/export_profile.js', sel_root=True)
        return self._driver.execute_async_script(js)




