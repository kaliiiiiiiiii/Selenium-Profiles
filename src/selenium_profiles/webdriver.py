import warnings
from collections import defaultdict
from selenium_profiles.utils.utils import valid_key

from selenium.webdriver.chrome.service import Service as ChromeService

from selenium_profiles.utils.colab_utils import is_colab
from selenium_profiles.scripts.cdp_tools import cdp_tools
from selenium_profiles.scripts.profiles import options as options_handler


# noinspection PyDefaultArgument
def Chrome(profile: dict = None,
           chrome_binary:str=None, executable_path:str = None,
           options = None, duplicate_policy: str = "warn-add", safe_duplicates: list = ["--add-extension"],
           uc_driver: bool or None = None, seleniumwire_options:dict or bool or None = None, base_driver=None,
           **kwargs):

    if base_driver and (uc_driver or seleniumwire_options):
        raise ValueError("uc_driver or seleniumwire can't be used with base_driver specified")

    # import webdriver
    if uc_driver:
        if seleniumwire_options:
            import seleniumwire.undetected_chromedriver as webdriver
        else:
            import undetected_chromedriver as webdriver
    else:
        if seleniumwire_options:
            from seleniumwire import webdriver
        else:
            from selenium import webdriver

    if not base_driver:
        base_driver = webdriver.Chrome

    if not options:
        if webdriver:
            options = webdriver.ChromeOptions()
        else:
            from selenium.webdriver import ChromeOptions
            options = ChromeOptions()

    class _Chrome(base_driver):
        # noinspection PyDefaultArgument
        def __init__(self, _profile: dict = None, _chrome_binary:str=None, _executable_path:str = None,
                 _options = None,_duplicate_policy: str = "warn-add", _safe_duplicates: list = ["--add-extension"],
                 _uc_driver: bool or None = None, _seleniumwire_options:dict or bool or None = None, **_kwargs):

            from selenium_profiles.scripts.profiles import cdp as cdp_handler

            if not _profile:
                _profile = {}

            valid_key(_profile.keys(), ["cdp", "options"], "profile (selenium-profiles)")

            if type(_seleniumwire_options) is dict:
                kwargs.update({"seleniumwire_options": _seleniumwire_options})
            elif not (type(_seleniumwire_options) is bool or _seleniumwire_options is None):
                raise ValueError("Expected NoneType, dict or bool")

            defdict = defaultdict(lambda: None)
            defdict.update(_profile)
            _profile = defdict

            # sandbox handling for google-colab
            if is_colab():
                # todo: nested default-dict with Lambda: None
                if _profile["options"]:
                    # noinspection PyUnresolvedReferences
                    if 'sandbox' in _profile["options"].keys():
                        # noinspection PyUnresolvedReferences
                        if _profile["options"]["sandbox"] is True:
                            warnings.warn('Google-colab doesn\'t work with sandbox enabled yet, disabling sandbox')
                    else:
                        # noinspection PyUnresolvedReferences
                        _profile["options"].update({"sandbox": False})
                else:
                    # noinspection PyTypeChecker
                    _profile.update({"options": {"sandbox": False}})

            # options-manager
            options_manager = options_handler(_options, _profile["options"], duplicate_policy=_duplicate_policy,
                                              safe_duplicates=_safe_duplicates)

            # chrome executable path
            if not chrome_binary:
                options_manager.Options.binary_location = chrome_binary

            # chromedriver path
            if uc_driver:
                if executable_path:
                    _kwargs.update({"driver_executable_path": self.executable_path})
            else:
                # detectability options
                from selenium_profiles.scripts import undetected

                # is adb used ?
                try:
                    # noinspection PyUnresolvedReferences
                    adb = _profile["options"]["adb"]
                except TypeError:
                    adb = None
                except KeyError:
                    adb = None

                options_manager.Options = undetected.config_options(options_manager.Options, adb=adb)

                # chromedriver path
                if executable_path:
                    _kwargs.update({"service": ChromeService(executable_path=self.executable_path)})

            # add options to kwargs
            _kwargs.update({"options": options_manager.Options})

            # Actual start of chrome
            super().__init__(**_kwargs)
            # cdp tools

            self.get("chrome://version/")  # wait browser to start

            _cdp_tools = cdp_tools(self)
            _cdp_tools.evaluate_on_document_identifiers.update({1:  # we know that it is there:)
                   """(function () {window.cdc_adoQpoasnfa76pfcZLmcfl_Array = window.Array;
                   window.cdc_adoQpoasnfa76pfcZLmcfl_Object = window.Object;
                   window.cdc_adoQpoasnfa76pfcZLmcfl_Promise = window.Promise;
                   window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy = window.Proxy;
                   window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol = window.Symbol;
                   }) ();"""})

            cdp_manager = cdp_handler(self, _cdp_tools)
            cdp_manager.apply(cdp_profile=profile["cdp"])

            if not uc_driver:
                from selenium_profiles.scripts import undetected
                undetected.exec_cdp(self, _cdp_tools)

            self.profiles = profiles(self, _profile,cdp_tools=cdp_tools,cdp_manager=cdp_manager)

    driver = _Chrome(_profile=profile,_chrome_binary=chrome_binary,_executable_path=executable_path,_options=options, _duplicate_policy=duplicate_policy, _safe_duplicates=safe_duplicates, _uc_driver=uc_driver, _seleniumwire_options=seleniumwire_options, **kwargs)
    return driver

class profiles:
    # noinspection PyShadowingNames
    def __init__(self, driver, profile, cdp_tools=None, cdp_manager=None):

        from selenium_interceptor.interceptor import cdp_listener
        from selenium_profiles.scripts.driver_utils import requests, actions
        from selenium_profiles.scripts.profiles import cdp as cdp_handler

        self._driver = driver
        self._profile = profile

        if cdp_tools:
            self.cdp_tools = cdp_tools
        else:
            from selenium_profiles.scripts.cdp_tools import cdp_tools
            self.cdp_tools = cdp_tools(self._driver)

        if cdp_manager:
            self.cdp_manager = cdp_manager
        else:
            self.cdp_manager = cdp_handler(self._driver, self.cdp_tools)

        self.cdp_listener = cdp_listener(driver=self._driver)
        self.actions = actions(self._driver)

        requests = requests(self._driver)
        self.fetch = requests.fetch

        # patch driver functions
        self._driver.get_cookies = self.cdp_tools.get_cookies
        self._driver.add_cookie = self.cdp_tools.add_cookie
        self._driver.get_cookie = self.cdp_tools.get_cookie
        self._driver.delete_cookie = self.cdp_tools.delete_cookie
        self._driver.delete_all_cookies = self.cdp_tools.delete_all_cookies

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
            self.cdp_manager.apply(profile["cdp"])

    def get_profile(self):
        from selenium_profiles.utils.utils import read
        js = read('js/export_profile.js', sel_root=True)
        return self._driver.execute_async_script(js)


