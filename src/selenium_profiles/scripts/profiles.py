import warnings
from collections import defaultdict
from typing import Dict  # define types in functions


class profiles:
    def __init__(self):
        self.cdp = self.cdp()
        self.options = self.options()

    class options: # webdriver.Chrome or uc.Chrome options
        def __init__(self):
            self.options = None
            self.device = self.device()
            self.browser = self.browser()
            self.extensions = self.extensions()

        # set options based on profile["options"] dict
        def set(self, options, options_profile: dict or None):
            self.options = options
            if options_profile:
                # noinspection PyShadowingNames
                profile = defaultdict(lambda: None)
                profile.update(options_profile)
                try:
                    # noinspection PyUnresolvedReferences
                    incognito = profile["browser"]["incognito"]
                except KeyError:  # doesn't exist..
                    incognito = None
                except  TypeError:
                    incognito = None

                extensions_used = profile["extensions"]

                self.device.set(self.options, option_device_profile=profile["device"])
                self.browser.set(self.options, option_browser_profile=profile["browser"],
                                 extensions_used=extensions_used, adb=profile["adb"])
                self.extensions.set(self.options, option_extension_profile=profile["extensions"], incognito=incognito)
                self.extend_options(self.options, profile["option_args"])
                self.extend_capabilities(self.options, capabilities=profile["capabilities"])
                # noinspection PyTypeChecker
                self.adb_remote(self.options, enabled=profile["adb"], package=profile["adb_package"],
                                use_running_app=profile["use_running_app"])

            return self.options

        class device:
            def __init__(self):
                self.options = None

            # noinspection PyTypeChecker
            def set(self,options, option_device_profile:None or dict):
                if option_device_profile:
                    # noinspection PyShadowingNames
                    profile = defaultdict(lambda: None)
                    profile.update(option_device_profile)
                    self.options = options

                    self.useragent(self.options,useragent=profile["useragent"])
                    self.mobile(self.options,enabled=profile["mobile"])
                return self.options
            def useragent(self, options, useragent:str=None):
                # gets overwritten by cdp, if cdp used
                if useragent:
                    options.add_argument('--user-agent=' + useragent)

                return options

            def mobile(self, options, enabled:bool or None = False):
                # not sure, if it changes anything?
                if enabled:
                    options.add_argument('--enable-features=enable-nacl')
                    options.add_argument('--arc-availability=officially-supported')
                    options.add_argument('--force-device-ownership')
                    options.add_argument('--use-mobile-user-agent')
                return options


        class browser:
            def __init__(self):
                self.options = None

            # noinspection PyTypeChecker
            def set(self, options, option_browser_profile: dict or None, extensions_used:bool=None, adb:bool=None):
                if option_browser_profile:
                    # noinspection PyShadowingNames
                    profile = defaultdict(lambda: None)
                    profile.update({'window_size':defaultdict(lambda: None)})
                    profile.update(option_browser_profile)
                    self.options = options

                    self.sandbox(self.options, enabled=profile["sandbox"])
                    self.window_size(self.options,size=profile["window_size"])
                    self.headless(self.options,headless=profile["headless"],load_images=profile["load_images"])
                    self.incognito(self.options,enabled=profile["incognito"],extension_used=extensions_used)
                    self.touch(self.options,enabled=profile["touch"])
                    self.app(self.options, enabled=profile["app"])
                    self.gpu(self.options, enabled=profile["gpu"], adb=adb)
                    self.mobile_view(self.options, enabled=profile["mobile_view"])
                    self.proxy(self.options, proxy=profile["proxy"], method=profile["proxy_method"])
                return self.options



            def sandbox(self,options, enabled:bool=True):
                if enabled is False:
                    options.arguments.extend(["--no-sandbox", "--test-type"])
                    options.add_argument('--enable-privacy-sandbox-ads-apis')
                    warnings.warn('Might be more likely to get detected with sandbox set to False!')
                return options

            # noinspection PyDefaultArgument
            def window_size(self,options,size:Dict[str,str] or None = {"x":1024,"y":648}):
                # only for Desktop
                if size:
                    options.add_argument("--window-size=" + str(size['x']) + "," + str(size['y']))
                return options

            def headless(self,options, headless:bool = False, load_images:bool = True):
                # ==> without Window
                # only for desktop
                if headless:
                    options.add_argument('--headless=chrome')
                if load_images is False:
                    options.add_argument("--blink-settings=imagesEnabled=false")
                return options

            def incognito(self, options, enabled:bool = True, extension_used:bool or None=False):
                # use Incognito
                # woking on Android?
                if enabled:
                    if not extension_used:
                        options.add_argument("--incognito")
                    else:
                        warnings.warn('Incognito not working with Extensions!, disabling Incognito')
                return options

            def touch(self, options, enabled: bool = True):
                if enabled:
                    options.add_argument("--touch-events=enabled")
                elif enabled is False:
                    options.add_argument("--touch-events=disabled")
                return options

            def app(self, options, enabled:bool=False):
                if enabled:
                    options.add_argument('--app')
                    options.add_argument('--force-app-mode')
                return options

            def gpu(self, options, enabled=False, adb:bool=None):
                if enabled is None:
                    enabled=True
                if not enabled:
                    if not adb or adb is None:
                        options.add_argument('--disable-gpu')
                        options.add_argument('--override-use-software-gl-for-tests')
                    else:
                        warnings.warn('Disabling gpu not supported with android.')
                return options

            def mobile_view(self, options, enabled:bool=False):
                if enabled:
                    options.add_argument('--enable-touchview')
                    warnings.warn('--enable-touchview doesn\t seem to change anything')
                return options

            def proxy(self,options, proxy:str =None, method:str = 'socks5://'):
                if not method:
                    method = "'socks5://'"
                if proxy:
                    options.add_argument('--proxy-server='+method + proxy)
                    print('proxy= "' + method+proxy + '"')
                return options

        def extend_options(self, options, input_options: list = None):
            if input_options:
                for arg in input_options:
                    options.add_argument(arg)
            return options

        def extend_capabilities(self, options, capabilities:list or None=None):
            if capabilities:
                for cap in capabilities:
                    options.set_capability(cap[0], cap[1])
            return options

        def adb_remote(self, options,enabled:bool or None=True, package:str='com.android.chrome', use_running_app:bool=None):
            if package is None: # default
                package = 'com.android.chrome'
            if enabled:
                options.add_experimental_option('androidPackage', package)
                if use_running_app or use_running_app is None:
                    options.add_experimental_option('androidUseRunningApp', True)

        class extensions:
            def __init__(self):
                self.options = None

            def set(self, options, option_extension_profile: None or dict, incognito:bool=None):
                if option_extension_profile:
                    # noinspection PyShadowingNames
                    profile = defaultdict(lambda : None)
                    profile.update(option_extension_profile)
                    self.options = options
                    auth_proxy = defaultdict(lambda: None)
                    # noinspection PyTypeChecker
                    auth_proxy.update(profile["auth_proxy"])

                    self.add_extension(self.options,profile["extension_paths"],incognito=incognito)
                    if auth_proxy:
                        # noinspection PyUnresolvedReferences,PyTypeChecker
                        self.add_auth_proxy(auth_proxy["host"], auth_proxy["port"], auth_proxy["username"], auth_proxy["password"], scheme=auth_proxy["scheme"])
                return self.options
            def add_extension(self, options, extension_paths:None or list, incognito:bool = None):
                if extension_paths:
                    if incognito:
                        warnings.warn('Incognito might not be compatible with extensions')
                    for extension_path in extension_paths:
                        if extension_path[-3:] == ".crx" or extension_path[-3:] == ".zip":
                            options.add_extension(extension_path)
                        else:
                            options.add_argument('--load-extension=' + extension_path)
                return options

            def add_auth_proxy(self,host:str, port:int, username:str or None, password:str or None, scheme:str or None= "http"):
                from selenium_profiles.scripts.proxy_extension import make_extension

                if not scheme:
                    scheme = "http"

                path = make_extension(host= host, port=port, username= str(username), password= str(password), scheme=scheme)
                self.add_extension(extension_paths=[path], options=self.options)

    # noinspection PyTypeChecker
    class cdp:
        def __init__(self):
            self.browser = self.browser()

        def set(self, driver, cdp_profile:bool or None = None):
            if cdp_profile:
                # noinspection PyShadowingNames
                profile = defaultdict(lambda: None)
                profile.update(cdp_profile)

                try:
                    # noinspection PyUnresolvedReferences
                    mobile = profile["emulation"]["mobile"]
                except KeyError:
                    mobile = False

                browser = self.browser.set(driver, profile["browser"], mobile=mobile)
                touchpoints = self.set_touchpoints(driver, enabled=profile["touch"], maxpoints=profile["maxtouchpoints"])
                emulation = self.set_emulation(driver, profile["emulation"])
                useragent = self.set_useragent(driver, profile["useragent"])

                cdp_args = profile["cdp_args"]
                cdp_args_return = []

                if cdp_args:
                    # noinspection PyUnresolvedReferences
                    if cdp_args[0]:
                        for args in cdp_args:
                            cdp_args_return.append(driver.execute_cdp_cmd(args[0], args[1]))

                return {"browser": browser, "touchpoints": touchpoints, "emulation": emulation, "useragent": useragent,
                        "cdp_args": cdp_args_return}

        def set_useragent(self, driver, useragent:dict = None):
            from selenium_profiles.scripts.cdp_tools import cdp_tools
            cdp_tools = cdp_tools(driver)
            if useragent:
                return cdp_tools.set_useragent(useragent=useragent)
        def set_emulation(self, driver, emulation:dict = None):
            from selenium_profiles.scripts.cdp_tools import cdp_tools
            cdp_tools = cdp_tools(driver)

            if emulation:
                return cdp_tools.set_emulation(emulation=emulation)

        def set_touchpoints(self, driver, enabled:bool=True, maxpoints:int=10):
            if maxpoints is None:
                maxpoints = 10
            if enabled is None:
                enabled=True
            from selenium_profiles.scripts.cdp_tools import cdp_tools
            cdp_tools = cdp_tools(driver)

            return cdp_tools.set_touchpoints(enabled=enabled, maxpoints=maxpoints)

        # noinspection PyTypeChecker
        class browser:

            def __init__(self):
                pass

            def set(self,driver, browser_cdp_profile, mobile=None):
                if browser_cdp_profile:
                    # noinspection PyShadowingNames
                    profile = defaultdict(lambda: None)
                    profile.update(browser_cdp_profile)

                    pointer_as_touch = self.pointer_as_touch(driver, enabled=profile["pointer_as_touch"], mobile=mobile)
                    darkmode = self.darkmode(driver, profile["darkmode"],mobile=profile["mobile"])
                    return {"pointer_as_touch": pointer_as_touch, "darkmode": darkmode}

            def pointer_as_touch(self,driver, enabled:None or bool=True, mobile:None or bool=True):
                from selenium_profiles.scripts.cdp_tools import cdp_tools
                cdp_tools = cdp_tools(driver)
                return cdp_tools.pointer_as_touch(mobile, enabled)

            def darkmode(self,driver,enabled:bool=True, mobile:bool=False):
                from selenium_profiles.scripts.cdp_tools import cdp_tools
                cdp_tools = cdp_tools(driver)
                return cdp_tools.set_darkmode(enabled=enabled, mobile=mobile)


# noinspection PyShadowingNames
def exec_js_evaluators(profile: dict, driver, cdp_tools=None):
    if cdp_tools:
        do_return = False
    else:
        from selenium_profiles.scripts.cdp_tools import cdp_tools
        cdp_tools = cdp_tools(driver)
        do_return = True

    # noinspection PyBroadException
    try:
        platform = profile["cdp"]["useragent"]["platform"]
    except :
        platform = None

    # noinspection PyBroadException
    try:
        max_touch_points = profile["cdp"]["maxtouchpoints"]
    except:
        max_touch_points = None


    if platform:
        cdp_tools.define_prop_on_new_document("navigator", "platform", platform)

    if max_touch_points:
        cdp_tools.define_prop_on_new_document('navigator','maxTouchPoints', max_touch_points)


    if do_return:
        return cdp_tools.evaluate_on_document_identifiers
