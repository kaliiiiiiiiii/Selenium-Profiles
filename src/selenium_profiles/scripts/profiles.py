import warnings
from collections import defaultdict
from typing import Dict  # define types in functions

from selenium_profiles.utils.utils import check_cmd, valid_key

class profiles:
    def __init__(self):
        pass
    class options:  # webdriver.Chrome or uc.Chrome options
        # noinspection PyDefaultArgument
        def __init__(self, options, options_profile: dict or None=None, dublicate_policy: str = "warn-add", safe_dublicates:list=["--add-extension"]):
            """
            :param options:  for example ChromeOptions()
            :param options_profile: # profile["options"] for a Selenium-Profiles profile
            :param dublicate_policy: for args | "raise" or "replace" or "warn-replace" or "skip" or "warn-skip" or "add" or "warn-add"
            exact dublicates always get removed with a warning
            """
            if not options_profile:
                options_profile = {}
            self.profile = defaultdict(lambda: None)
            self.profile.update(options_profile)

            self.dublicate_policy = dublicate_policy
            self.dublicates = defaultdict(lambda:set())
            self.safe_dublicates = safe_dublicates


            self.Options = options
            self.to_capabilities = self.Options.to_capabilities

            self._profile_keys = ["sandbox", "window_size", "headless", "load_images", "incognito", "touch", "app", "gpu",
                                 "proxy","args","capabilities","experimental_options","adb","adb_package","use_running_app",
                                 "extension_paths", "auth_proxy"
                                  ]
            self._supported_dublicate_policies = ["raise", "replace", "warn-replace",
                                                 "skip", "warn-skip", "add", "warn-add"]

            self.apply(options_profile)
        def apply(self, options_profile):
            profile = defaultdict(lambda :None)
            profile.update(options_profile)

            valid_key(profile.keys(), self._profile_keys, "options_profile => profile['options']")
            # libs
            self.sandbox(enabled=profile["sandbox"], adb=profile["adb"])
            self.window_size(profile["window_size"], adb=profile["adb"])
            self.headless(profile["headless"],profile["load_images"])
            self.incognito(profile["incognito"],profile["extensions"])
            self.touch(profile["touch"])
            self.app(profile["app"],adb=profile["adb"])
            self.gpu(profile["gpu"],adb=profile["adb"])
            self.proxy(profile["proxy"])
            self.extend_arguments(profile["args"])
            self.update_capabilities(profile["capabilities"])
            self.update_experimental_options(profile["experimental_options"])
            self.adb_remote(profile["adb"], package=profile["adb_package"], use_running_app=profile["use_running_app"])
            self.add_extensions(profile["extension_paths"], adb=profile["adb"])
            self.auth_proxy(profile["auth_proxy"])
            return self.Options

        # noinspection PyIncorrectDocstring
        def sandbox(self, enabled: bool or None = None, adb:bool or None=None):
            """
            :param enabled: defaults to True
            """
            if enabled is False:
                self.warn_adb_unsupported(adb, "disabling sandbox")
                self.extend_arguments(["--no-sandbox", "--test-type"])

        # noinspection PyDefaultArgument
        def window_size(self, size: Dict[str, str] or None = None, adb:bool or None = None):
            """
            :param size: defaults to default
            :param adb: warning
            """
            if size:
                self.warn_adb_unsupported(adb, "setting window_size")
                if "x" not in size.keys():
                    raise ValueError("value 'x' is required for specifying window_size")
                if "y" not in size.keys():
                    raise ValueError("value 'y' is required for specifying window_size")
                valid_key(size.keys(), ["x", "y"], 'profile_options window_size => profile["options"]["window_size]')
                self.add_argument("--window-size=" + str(size['x']) + "," + str(size['y']))

        # noinspection PyIncorrectDocstring
        def headless(self, headless: bool or None = None, load_images: bool or None = None, adb:bool or None=None):
            """
            :param headless: defaults to False
            :param load_images: defaults to True
            """

            if headless:
                self.warn_adb_unsupported(adb, "enabling headless")
                self.add_argument('--headless=new')
            if load_images is False:
                self.warn_adb_unsupported(adb, "disabling images")
                self.add_argument("--blink-settings=imagesEnabled=false")

        # noinspection PyIncorrectDocstring
        def incognito(self,enabled: bool or None = False, extension_used: bool or None = None, adb:bool or None=None):
            """
            :param enabled: incognito defaults to False
            :param extension_used: defaults to False

            prints warning if extensions are used
            """
            if enabled:
                self.warn_adb_unsupported(adb, "enabling incognito")
                if extension_used:
                    warnings.warn('Incognito is rarely working with Extensions.')
                self.add_argument("--incognito")



        def touch(self, enabled: bool or None = None):
            """
            :param enabled: defaults to default
            """

            if enabled is False:
                self.add_argument("--touch-events=disabled")
            elif enabled is True:
                self.add_argument("--touch-events=enabled")

        # noinspection PyIncorrectDocstring
        def app(self,enabled: bool or None = None, adb:bool or None = None):
            """
            :param enabled: defaults to False

            disables some Desktop window features
            """

            if enabled is True:
                self.warn_adb_unsupported(adb, "enabling app view")
                self.add_argument('--app')
                self.add_argument('--force-app-mode')

        def gpu(self, enabled: bool or None = None, adb: bool or None = None):
            """
            disables GPU for Chrome
            :param enabled: defaults to True
            :param adb: defaults to False

            Not supported on Android Hardware
            """

            if enabled is False:
                if not adb:
                    self.add_argument('--disable-gpu')
                    self.add_argument('--override-use-software-gl-for-tests')
                else:
                    warnings.warn('Disabling GPU not supported when running on Android hardware, skipping')

        def adb_remote(self, enabled: bool or None = None, package: str or None = None,
                       use_running_app: bool = None):
            """
            :param enabled: defaults to False
            :param package: defaults to 'com.android.chrome'
            :param use_running_app: defaults to True
            """

            if package is None:  # default
                package = 'com.android.chrome'
            if enabled:
                self.update_experimental_options({'androidPackage': package})
                if use_running_app or use_running_app is None:
                    self.update_experimental_options({'androidUseRunningApp': True})

        def warn_adb_unsupported(self, adb:bool or None, methdod:str):
            if adb:
                warnings.warn(f"specifying {methdod} not supported on Android hardware")



        def proxy(self, proxy: str = None):
            """
            :param proxy: scheme://host:port => https://example.com:9000
            """
            supported_schemes = ["http", "https", "socks4", "socks5"]

            if proxy:
                scheme = proxy.split("://")
                check_cmd(scheme, supported_schemes)
                if "@" in proxy:
                    raise ValueError("Proxies specified in options don't allow authentification")
                self.add_argument('--proxy-server=' + proxy)






        ## tools ##

        def extend_arguments(self, my_args: list = None, dublicate_policy=None):

            if my_args:
                for arg in my_args:
                    self.add_argument(arg, dublicate_policy=dublicate_policy)

        def add_argument(self, my_option: str, dublicate_policy=None):
            """
            :param my_option: argument to add
            :param dublicate_policy: "raise" or "replace" or "warn-replace" or "skip" or "warn-skip" or "add" or "warn-add"
            """

            if dublicate_policy:
                policy = dublicate_policy
            else:
                policy = self.dublicate_policy

            check_cmd(policy, self._supported_dublicate_policies)
            my_arg = my_option.split("=")[0]
            dublicates_found = False
            # iterateover current options
            if self.Options.arguments:
                for i, option in list(enumerate(self.Options.arguments)):
                    arg = option.split("=")[0]

                    if my_arg == arg:  # got dublicate
                        if my_option == option:
                            warnings.warn(f"exact dublicate found for {my_option}, skipping")
                            return
                        else:
                            dublicates_found = True
                            if my_arg not in self.safe_dublicates:
                                self.dublicates[arg].update({my_option, option})
                                # replace
                                if policy == "replace":
                                    self.Options.arguments[i] = my_option
                                elif policy == "warn-replace":
                                    self.Options.arguments[i] = my_option
                                    warnings.warn(f"found dublicate for {my_option}: {option} , replacing")
                                # skipp
                                elif policy == "skip":
                                    pass
                                elif policy == "warn-skip":
                                    warnings.warn(f"found dublicate for {my_option}: {option}, skipping")

                                # raise
                                elif policy == "raise":
                                    raise ValueError(f"found dublicate for {my_option}: {option}")
                    else:
                        self.Options.arguments.append(my_option)
                        return

                # add
                if dublicates_found: # we only want to add them once:)
                    if my_arg in self.safe_dublicates:
                        self.Options.arguments.append(my_option)
                        return
                    if policy == "add":
                        self.Options.arguments.append(my_option)
                    elif policy == "warn-add":
                        self.Options.arguments.append(my_option)
                        warnings.warn(f"found dublicates for {my_option}: {self.dublicates[my_arg]} , adding")

            else: # first option to add
                self.Options.arguments.append(my_option)


        def update_capabilities(self, capabilities: dict or None = None, dublicate_policy=None):
            """
            :param dublicate_policy: self._supported_dublicate_policies
            :param capabilities: dict of {"capability":value}

            handling of dublicates not implemented yet!
            """
            if dublicate_policy:
                policy = dublicate_policy
            else:
                policy = self.dublicate_policy


            if capabilities:
                check_cmd(policy, self._supported_dublicate_policies)
                for cap, value in capabilities.items():
                    if cap in self.Options.capabilities.keys():
                        dublicate = self.Options.capabilities[cap]
                        if policy == "replace":
                            self.Options.set_capability(cap, value=value)
                        elif policy == "warn-replace":
                            self.Options.set_capability(cap, value=value)
                            warnings.warn(f"got dublicate for {cap}: {dublicate} , replacing")
                        # skipp
                        elif policy == "skip":
                            pass
                        elif policy == "warn-skip":
                            warnings.warn(f"got dublicate for {cap}: {dublicate}, skipping")
                        elif policy =="add" or policy == "warn-add":
                            warnings.warn(f"got dublicate for {cap}: {dublicate} ,policy is {policy}, but capabilties need to be unique, skipping")
                        # raise
                        elif policy == "raise":
                            raise ValueError(f"got dublicate for {cap}: {dublicate}")
                    else:
                        self.Options.set_capability(cap, value=value)
        def update_experimental_options(self, experimental_options: dict or None = None, dublicate_policy=None):
            """
            :param experimental_options: dict of {"experimental_option":value}
            :param dublicate_policy: self._supported_dublicate_policies
            """
            if dublicate_policy:
                policy = dublicate_policy
            else:
                policy = self.dublicate_policy


            if experimental_options:
                check_cmd(policy, self._supported_dublicate_policies)
                for key, value in experimental_options.items():
                    if key in self.Options.experimental_options.keys():
                        dublicate = self.Options.experimental_options[key]
                        if policy == "replace":
                            self.Options.add_experimental_option(key, value=value)
                        elif policy == "warn-replace":
                            self.Options.add_experimental_option(key, value=value)
                            warnings.warn(f"got dublicate for {key}: {dublicate} , replacing")
                        # skipp
                        elif policy == "skip":
                            pass
                        elif policy == "warn-skip":
                            warnings.warn(f"got dublicate for {key}: {dublicate}, skipping")
                        elif policy =="add" or policy == "warn-add":
                            warnings.warn(f"got dublicate for {key}: {dublicate} ,policy is {policy}, but experimental_options need to be unique, skipping")
                        # raise
                        elif policy == "raise":
                            raise ValueError(f"got dublicate for {key}: {dublicate}")
                    else:
                        self.Options.add_experimental_option(key, value=value)




        # extensions
        def add_extensions(self, extension_paths: None or list=None, adb:bool or None = None):
            """
            :param adb: adding extensions not supported when running on Android hardware
            :param extension_paths: list of paths to add extension from
            """

            import os
            if extension_paths:
                if adb:
                    raise ValueError("adding extensions not supported when running on Android hardware")
                for extension_path in extension_paths:
                    file_type = extension_path[-4:]
                    if os.path.exists(extension_path):
                        if os.path.isfile(extension_path):
                            if not(file_type == ".crx" or file_type == ".zip"):
                                warnings.warn("Extension-file isn't *.zip or *.crx")
                            self.Options.add_extension(extension_path)
                        elif os.path.isdir(extension_path):
                            self.add_argument('--load-extension=' + extension_path)
                    else:
                        raise LookupError("Extension-path doesn't exsist")

        def auth_proxy(self, config:dict = None):
            """
            :param config: dict =>
            {
            host: str
            port: int
            username: str | optional
            password: str | optional
            scheme: str | optional
            temp_dir: str | optional
            }
            """
            from selenium_profiles.scripts.proxy_extension import make_extension

            if config:
                auth_proxy = defaultdict(lambda: None)
                auth_proxy.update(config)

                valid_key(auth_proxy.keys(), ["host", "port", "username", "password", "scheme", "temp_dir"],
                          'profile_options auth_proxy => profile["options"]["auth_proxy"]')

                host = auth_proxy["host"]
                port = auth_proxy["port"]
                username = auth_proxy["username"]
                password = auth_proxy["password"]
                scheme = auth_proxy["scheme"]
                temp_dir = auth_proxy["temp_dir"]

                if not host:
                    raise ValueError("value 'host' is required")
                if not port:
                    raise ValueError("value 'port' is required")

                if not scheme:
                    scheme = "http"

                # noinspection PyTypeChecker
                path = make_extension(host=host, port=port, username=str(username), password=str(password),
                                      scheme=scheme, temp_dir=temp_dir)
                self.add_extensions(extension_paths=[path])

    # noinspection PyTypeChecker
    class cdp:
        def __init__(self, driver, cdp_tools=None):
            self._driver = driver

            if not cdp_tools:
                from selenium_profiles.scripts.cdp_tools import cdp_tools
                cdp_tools = cdp_tools(self._driver)

            self.cdp_tools = cdp_tools
            self.browser = self.browser(self._driver, self.cdp_tools)

        def apply(self, cdp_profile: bool or None = None):
            if cdp_profile:
                # noinspection PyShadowingNames
                profile = defaultdict(lambda: None)
                profile.update(cdp_profile)

                # is mobile ?
                try:
                    # noinspection PyUnresolvedReferences
                    mobile = profile["emulation"]["mobile"]
                except KeyError:
                    mobile = False
                except TypeError:
                    mobile = False

                # libs
                browser = self.browser.apply(profile["browser"], mobile=mobile)
                touchpoints = self.set_touchpoints(enabled=profile["touch"],
                                                   maxpoints=profile["maxtouchpoints"])
                emulation = self.set_emulation(profile["emulation"])
                useragent = self.set_useragent(profile["useragent"], patch_version=profile["patch_version"])
                cores = self.set_cores(cores_count=profile["cores"])

                # execute list of cdp args
                cdp_args_return = []
                cdp_args = profile["cdp_args"]
                if not cdp_args:
                    cdp_args = {}
                if cdp_args:
                    # noinspection PyUnresolvedReferences
                    if cdp_args[0]:
                        for arg, value in cdp_args.items():
                            cdp_args_return.append(self._driver.execute_cdp_cmd(arg, value))

                return {"browser": browser, "touchpoints": touchpoints, "emulation": emulation, "useragent": useragent,
                        "cores": cores,
                        "cdp_args": cdp_args_return}

        def set_useragent(self, useragent: dict = None, patch_version: str or bool = None):
            useragent = self.patch_version(useragent_profile=useragent, version=patch_version, driver = self._driver)
            if useragent:
                return self.cdp_tools.set_useragent(useragent=useragent)

        def patch_version(self, useragent_profile: dict, version: str or True = True, driver=None):
            """
            :param useragent_profile: profile["cdp"]["useragent"]
            :param version: string or True (and driver specified => automatically get version)
            :param driver: driver object to authomatically get the version
            :return: patched useragent_profile => profile["cdp"]["useragent"]
            """
            profile = defaultdict(lambda: None)
            profile.update(useragent_profile)

            if version is True:
                if driver:
                    useragent = driver.execute_script("return navigator.userAgent")
                    import re
                    version = re.findall("(?<=Chrome/)\d+(?:\.\d+)+|(?<=Chromium/)\d+(?:\.\d+)+", useragent)
                    if len(version) != 1:
                        raise LookupError("Couldn't find Chrome-version in: " + useragent)
                    else:
                        version = version[0]
                else:
                    raise ValueError("driver or version needs to be specified")

            if type(version) == str:
                if profile["userAgent"]:
                    import re
                    profile["userAgent"] = re.sub("(?<=Chrome/)\d+(?:\.\d+)+|(?<=Chromium/)\d+(?:\.\d+)+",
                                                  version.split(".")[0] + ".0.0.0", profile["userAgent"])

                if profile["userAgentMetadata"]:
                    metadata = defaultdict(lambda: None)
                    metadata.update(profile["userAgentMetadata"])

                    if metadata["brands"]:
                        brands = []
                        for brand in metadata["brands"]:
                            if not (brand["brand"] == "Not=A?Brand" or brand["brand"] == "Not)A;Brand"):
                                brand["version"] = version.split(".")[0]
                            brands.append(brand)
                        metadata["brands"] = brands

                    if metadata["fullVersionList"]:
                        version_list = []
                        for i in metadata["fullVersionList"]:
                            if not (i["brand"] == "Not=A?Brand" or i["brand"] == "Not)A;Brand"):
                                i["version"] = version
                            version_list.append(i)
                        metadata["fullVersionList"] = version_list

                    if metadata["fullVersion"]:
                        metadata["fullVersion"] = version

                    profile["userAgentMetadata"] = metadata

            return profile

        def set_emulation(self, emulation: dict = None):

            if emulation:

                if not "screenWidth" in emulation.keys():
                    emulation.update({"screenWidth": emulation["width"]})
                if not "screenHeight" in emulation.keys():
                    emulation.update({"screenHeight": emulation["height"]})

                return self.cdp_tools.set_emulation(emulation=emulation)

        def set_touchpoints(self, enabled: bool = True, maxpoints: int = 10):
            if maxpoints is None:
                maxpoints = 10
            if enabled is None:
                enabled = True

            return self.cdp_tools.set_touchpoints(enabled=enabled, maxpoints=maxpoints)

        def set_cores(self, cores_count: int or None = 8):
            if cores_count:
                return self.cdp_tools.set_cores(cores_count=cores_count)

        # noinspection PyTypeChecker
        class browser:

            def __init__(self, driver, cdp_tools):
                self._driver = driver
                self._cdp_tools = cdp_tools

            def apply(self, browser_cdp_profile, mobile=None):
                if browser_cdp_profile:
                    # noinspection PyShadowingNames
                    profile = defaultdict(lambda: None)
                    profile.update(browser_cdp_profile)

                    pointer_as_touch = self.pointer_as_touch(enabled=profile["pointer_as_touch"], mobile=mobile)
                    darkmode = self.darkmode(profile["darkmode"], mobile=profile["mobile"])
                    return {"pointer_as_touch": pointer_as_touch, "darkmode": darkmode}

            def pointer_as_touch(self, enabled: None or bool = True, mobile: None or bool = True):
                return self._cdp_tools.pointer_as_touch(mobile, enabled)

            def darkmode(self, enabled: bool = True, mobile: bool = False):
                return self._cdp_tools.set_darkmode(enabled=enabled, mobile=mobile)
