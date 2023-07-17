import warnings
from collections import defaultdict
from typing import Dict

from selenium_profiles.utils.utils import check_cmd, valid_key


class cdp_handler:
    def __init__(self, driver):
        self._driver = driver

        self._supported_keys = ["touch", "maxtouchpoints", "emulation", "useragent", "patch_version",
                                "cores", "darkmode","pinter_as_touch","cdp_args"]

        self.evaluate_on_document_identifiers = {}

    def apply(self, cdp_profile: bool or None = None):
        """
        :param cdp_profile: => profile["cdp"]
        """
        if cdp_profile:
            # noinspection PyShadowingNames
            profile = defaultdict(lambda: None)
            profile.update(cdp_profile)

            valid_key(cdp_profile.keys(), self._supported_keys, 'cdp_profile => profile["cdp"]')

            # is mobile ?
            try:
                # noinspection PyUnresolvedReferences
                mobile = profile["emulation"]["mobile"]
            except KeyError:
                mobile = False
            except TypeError:
                mobile = False

            # libs
            touchpoints = self.set_touchpoints(enabled=profile["touch"], maxpoints=profile["maxtouchpoints"])
            emulation = self.set_emulation(profile["emulation"])
            useragent = self.set_useragent(profile["useragent"], patch_version=profile["patch_version"])
            cores = self.set_cores(cores_count=profile["cores"])
            darkmode = self.darkmode(profile["darkmode"], mobile=mobile)
            pointer_as_touch = self.pointer_as_touch(profile["pinter_as_touch"], mobile=mobile)
            cdp_args = self.execute_cdp_args(profile["cdp_args"])

            # execute list of cdp args


            return {"touchpoints": touchpoints, "emulation": emulation, "useragent": useragent,
                    "cores": cores,"pointer_as_touch":pointer_as_touch,"darkmode":darkmode,"cdp_args": cdp_args}

    def execute_cdp_args(self, cdp_args:dict or None = None):
        """
        :param cdp_args: dict of cdp_args => {"arg1":"value1", "arg2":"value2"}
        """
        cdp_args_return = []
        if not cdp_args:
            cdp_args = {}
        if cdp_args:
            if cdp_args[0]:
                for arg, value in cdp_args.items():
                    cdp_args_return.append(self._driver.execute_cdp_cmd(arg, value))
        return cdp_args_return

    def set_useragent(self, useragent: dict or None = None, patch_version: str or bool = None):
        """
        :param useragent: => https://chromedevtools.github.io/devtools-protocol/tot/Emulation/#method-setUserAgentOverride
            dict:
            {
                "userAgent":str,
                "acceptLanguage":optional-str,
                "platform":optional-str | => navigator.platform,
                "userAgentMetadata":optional-dict | =>  https://chromedevtools.github.io/devtools-protocol/tot/Emulation/#type-UserAgentMetadata
            }
        :param patch_version: True=> automatically patch, str => patch with string
        """
        if useragent:
            useragent = self.patch_version(useragent_profile=useragent, version=patch_version, driver=self._driver)
            return self._driver.execute_cdp_cmd('Emulation.setUserAgentOverride', useragent)

    def patch_version(self, useragent_profile: dict, version: str or bool or None = True, driver=None):
        """
        :param useragent_profile: profile["cdp"]["useragent"]
        :param version: string or True (and driver specified => automatically get version)
        :param driver: driver object to automatically get the version
        :return: patched useragent_profile => profile["cdp"]["useragent"]
        """
        profile = defaultdict(lambda: None)
        profile.update(useragent_profile)

        if version is True:
            if driver:
                useragent = driver.execute_cdp_cmd("Browser.getVersion",{})["product"]
                import re
                version = re.findall(r'(?<=Chrome/)\d+(?:\.\d+)+|(?<=Chromium/)\d+(?:\.\d+)+', useragent)
                version = version[0]
            else:
                raise ValueError("driver or version needs to be specified")

        if type(version) == str:
            if profile["userAgent"]:
                import re
                # noinspection PyTypeChecker
                profile["userAgent"] = re.sub(r"(?<=Chrome/)\d+(?:\.\d+)+|(?<=Chromium/)\d+(?:\.\d+)+",
                                              version.split(".")[0] + ".0.0.0", profile["userAgent"])

            if profile["userAgentMetadata"]:
                metadata = defaultdict(lambda: None)
                # noinspection PyTypeChecker
                metadata.update(profile["userAgentMetadata"])

                brands_pattern = r'^Not[ (:-./);=?_]A[ (:-./);=?_]Brand$'
                if metadata["brands"]:
                    brands = []
                    # noinspection PyTypeChecker
                    for brand in metadata["brands"]:
                        if not re.match(brands_pattern, brand["brand"]):
                            brand["version"] = version.split(".")[0]
                        brands.append(brand)
                    # noinspection PyTypeChecker
                    metadata["brands"] = brands

                if metadata["fullVersionList"]:
                    version_list = []
                    # noinspection PyTypeChecker
                    for i in metadata["fullVersionList"]:
                        if not re.match(brands_pattern, i["brand"]):
                            i["version"] = version
                        version_list.append(i)
                    # noinspection PyTypeChecker
                    metadata["fullVersionList"] = version_list

                if metadata["fullVersion"]:
                    metadata["fullVersion"] = version

                # noinspection PyTypeChecker
                profile["userAgentMetadata"] = metadata

        return profile

    def set_emulation(self, emulation: dict or None = None):
        """
        :param emulation: dict => https://chromedevtools.github.io/devtools-protocol/tot/Emulation/#method-setDeviceMetricsOverride
        """

        if emulation:

            # fix for https://github.com/kaliiiiiiiiii/Selenium-Profiles/issues/29
            if not "screenWidth" in emulation.keys():
                emulation.update({"screenWidth": emulation["width"]})
            if not "screenHeight" in emulation.keys():
                emulation.update({"screenHeight": emulation["height"]})

            return self._driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', emulation)

    def clear_emulation(self, enabled:bool or None):
        if enabled or (enabled is None):
            self._driver.execute_cdp_cmd("Emulation.clearDeviceMetricsOverride", {})

    def set_touchpoints(self, enabled: bool or None = None, maxpoints: int or None = None):
        """
        :param enabled:bool
        :param maxpoints:int
        """
        if not enabled is None:
            if maxpoints is None:
                maxpoints = 10
            return self._driver.execute_cdp_cmd('Emulation.setTouchEmulationEnabled',
                                                {'enabled': enabled, 'maxTouchPoints': maxpoints})

    def set_cores(self, cores_count: int or None = 8):
        """
        :param cores_count: int => navigator.hardwareConcurrency
        """
        if cores_count:
            return self._driver.execute_cdp_cmd("Emulation.setHardwareConcurrencyOverride",
                                                {"hardwareConcurrency": cores_count})


    def darkmode(self, enabled: bool or None = None, mobile: bool = False):
        if not enabled is None:
            if enabled:
                if not mobile:
                    warnings.warn('darkmode might look weird without mobile_view!')
                return self._driver.execute_cdp_cmd('Emulation.setAutoDarkModeOverride',
                                                    {'enabled': enabled})

    def pointer_as_touch(self, enabled: None or bool = True, mobile: bool = None):
        if mobile or mobile is None:
            config = 'mobile'
        else:
            config = 'desktop'
        if not(enabled is None):
            warnings.warn('Actions execute, but then take long when "EmitTouchEventsForMouse"!')
            # executes, but then takes long [maybe check if success?]
            return self._driver.execute_cdp_cmd('Emulation.setEmitTouchEventsForMouse', {'enabled': enabled,
                                                                                         'configuration': config})

    def evaluate_on_new_document(self, js: str):  # evaluate js on every new page
        identifier = int(
            self._driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})["identifier"])
        self.evaluate_on_document_identifiers.update({identifier: js})
        return identifier

    # remove js evaluation  on every new page for specific script
    def remove_evaluate_on_document(self, identifier: int):
        del self.evaluate_on_document_identifiers[identifier]
        return self._driver.execute_cdp_cmd("Page.removeScriptToEvaluateOnNewDocument", {"identifier": str(identifier)})

class options:  # webdriver.Chrome or uc.Chrome options
    # noinspection PyDefaultArgument,PyShadowingNames
    def __init__(self, options, options_profile: dict or None = None, duplicate_policy: str = "warn-add",
                 safe_duplicates: list = ["--add-extension"]):
        """
        :param options:  for example ChromeOptions()
        :param options_profile: # profile["options"] for a Selenium-Profiles profile
        :param duplicate_policy: for args | "raise" or "replace" or "warn-replace" or "skip" or "warn-skip" or "add" or "warn-add"
        exact duplicates always get removed with a warning
        """
        if not options_profile:
            options_profile = {}
        self.profile = defaultdict(lambda: None)
        self.profile.update(options_profile)

        self.duplicate_policy = duplicate_policy
        self.duplicates = defaultdict(lambda: set())
        self.safe_duplicates = safe_duplicates

        self.Options = options
        self.to_capabilities = self.Options.to_capabilities

        self._profile_keys = ["sandbox", "window_size", "headless", "load_images", "incognito", "touch", "app", "gpu",
                              "proxy", "args", "capabilities", "experimental_options", "adb", "adb_package",
                              "use_running_app",
                              "extension_paths",
                              ]
        self._supported_duplicate_policies = ["raise", "replace", "warn-replace",
                                              "skip", "warn-skip", "add", "warn-add"]

        self.apply(options_profile)

    def apply(self, options_profile):
        profile = defaultdict(lambda: None)
        profile.update(options_profile)

        valid_key(profile.keys(), self._profile_keys, "options_profile => profile['options']")
        # libs
        self.sandbox(enabled=profile["sandbox"], adb=profile["adb"])
        self.window_size(profile["window_size"], adb=profile["adb"])
        self.headless(profile["headless"], profile["load_images"])
        self.incognito(profile["incognito"], profile["extensions"])
        self.touch(profile["touch"])
        self.app(profile["app"], adb=profile["adb"])
        self.gpu(profile["gpu"], adb=profile["adb"])
        self.proxy(profile["proxy"])
        self.extend_arguments(profile["args"])
        self.update_capabilities(profile["capabilities"])
        self.update_experimental_options(profile["experimental_options"])
        self.adb_remote(profile["adb"], package=profile["adb_package"], use_running_app=profile["use_running_app"])
        self.add_extensions(profile["extension_paths"], adb=profile["adb"])
        return self.Options

    # noinspection PyIncorrectDocstring
    def sandbox(self, enabled: bool or None = None, adb: bool or None = None):
        """
        :param enabled: defaults to True
        """
        if enabled is False:
            self.warn_adb_unsupported(adb, "disabling sandbox")
            self.extend_arguments(["--no-sandbox", "--test-type"])

    # noinspection PyDefaultArgument
    def window_size(self, size: Dict[str, str] or None = None, adb: bool or None = None):
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
    def headless(self, headless: bool or None = None, load_images: bool or None = None, adb: bool or None = None):
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
    def incognito(self, enabled: bool or None = False, extension_used: bool or None = None, adb: bool or None = None):
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
    def app(self, enabled: bool or None = None, adb: bool or None = None):
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

    def warn_adb_unsupported(self, adb: bool or None, method: str):
        if adb:
            warnings.warn(f"specifying {method} not supported on Android hardware")

    def proxy(self, proxy: str = None):
        """
        :param proxy: scheme://host:port => https://example.com:9000
        """
        supported_schemes = ["http", "https", "socks4", "socks5"]

        if proxy:
            scheme = proxy.split("://")[0]
            check_cmd(scheme, supported_schemes)
            if "@" in proxy:
                raise ValueError("Proxies specified in options don't allow authentification")
            self.add_argument('--proxy-server=' + proxy)

    ## tools ##

    def extend_arguments(self, my_args: list = None, duplicate_policy=None):

        if my_args:
            for arg in my_args:
                self.add_argument(arg, duplicate_policy=duplicate_policy)

    def add_argument(self, my_option: str, duplicate_policy=None):
        """
        :param my_option: argument to add
        :param duplicate_policy: "raise" or "replace" or "warn-replace" or "skip" or "warn-skip" or "add" or "warn-add"
        """

        if duplicate_policy:
            policy = duplicate_policy
        else:
            policy = self.duplicate_policy

        check_cmd(policy, self._supported_duplicate_policies)
        my_arg = my_option.split("=")[0]
        duplicates_found = False
        # iterateover current options
        if self.Options.arguments:
            for i, option in list(enumerate(self.Options.arguments)):
                arg = option.split("=")[0]

                if my_arg == arg:  # got duplicate
                    if my_option == option:
                        warnings.warn(f"exact duplicate found for {my_option}, skipping")
                        return
                    else:
                        duplicates_found = True
                        if my_arg not in self.safe_duplicates:
                            self.duplicates[arg].update({my_option, option})
                            # replace
                            if policy == "replace":
                                self.Options.arguments[i] = my_option
                            elif policy == "warn-replace":
                                self.Options.arguments[i] = my_option
                                warnings.warn(f"found duplicate for {my_option}: {option} , replacing")
                            # skipp
                            elif policy == "skip":
                                pass
                            elif policy == "warn-skip":
                                warnings.warn(f"found duplicate for {my_option}: {option}, skipping")

                            # raise
                            elif policy == "raise":
                                raise ValueError(f"found duplicate for {my_option}: {option}")
                else:
                    self.Options.arguments.append(my_option)
                    return

            # add
            if duplicates_found:  # we only want to add them once:)
                if my_arg in self.safe_duplicates:
                    self.Options.arguments.append(my_option)
                    return
                if policy == "add":
                    self.Options.arguments.append(my_option)
                elif policy == "warn-add":
                    self.Options.arguments.append(my_option)
                    warnings.warn(f"found duplicates for {my_option}: {self.duplicates[my_arg]} , adding")

        else:  # first option to add
            self.Options.arguments.append(my_option)

    def update_capabilities(self, capabilities: dict or None = None, duplicate_policy=None):
        """
        :param duplicate_policy: self._supported_duplicate_policies
        :param capabilities: dict of {"capability":value}

        handling of duplicates not implemented yet!
        """
        if duplicate_policy:
            policy = duplicate_policy
        else:
            policy = self.duplicate_policy

        if capabilities:
            check_cmd(policy, self._supported_duplicate_policies)
            for cap, value in capabilities.items():
                if cap in self.Options.capabilities.keys():
                    duplicate = self.Options.capabilities[cap]
                    if policy == "replace":
                        self.Options.set_capability(cap, value=value)
                    elif policy == "warn-replace":
                        self.Options.set_capability(cap, value=value)
                        warnings.warn(f"got duplicate for {cap}: {duplicate} , replacing")
                    # skipp
                    elif policy == "skip":
                        pass
                    elif policy == "warn-skip":
                        warnings.warn(f"got duplicate for {cap}: {duplicate}, skipping")
                    elif policy == "add" or policy == "warn-add":
                        warnings.warn(
                            f"got duplicate for {cap}: {duplicate} ,policy is {policy}, but capabilties need to be unique, skipping")
                    # raise
                    elif policy == "raise":
                        raise ValueError(f"got duplicate for {cap}: {duplicate}")
                else:
                    self.Options.set_capability(cap, value=value)

    def update_experimental_options(self, experimental_options: dict or None = None, duplicate_policy=None):
        """
        :param experimental_options: dict of {"experimental_option":value}
        :param duplicate_policy: self._supported_duplicate_policies
        """
        if duplicate_policy:
            policy = duplicate_policy
        else:
            policy = self.duplicate_policy

        if experimental_options:
            check_cmd(policy, self._supported_duplicate_policies)
            for key, value in experimental_options.items():
                if key in self.Options.experimental_options.keys():
                    duplicate = self.Options.experimental_options[key]
                    if policy == "replace":
                        self.Options.add_experimental_option(key, value=value)
                    elif policy == "warn-replace":
                        self.Options.add_experimental_option(key, value=value)
                        warnings.warn(f"got duplicate for {key}: {duplicate} , replacing")
                    # skipp
                    elif policy == "skip":
                        pass
                    elif policy == "warn-skip":
                        warnings.warn(f"got duplicate for {key}: {duplicate}, skipping")
                    elif policy == "add" or policy == "warn-add":
                        warnings.warn(
                            f"got duplicate for {key}: {duplicate} ,policy is {policy}, but experimental_options need to be unique, skipping")
                    # raise
                    elif policy == "raise":
                        raise ValueError(f"got duplicate for {key}: {duplicate}")
                else:
                    self.Options.add_experimental_option(key, value=value)

    # extensions
    def add_extensions(self, extension_paths: None or list = None, adb: bool or None = None):
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
                        if not (file_type == ".crx" or file_type == ".zip"):
                            warnings.warn("Extension-file isn't *.zip or *.crx")
                        self.Options.add_extension(extension_path)
                    elif os.path.isdir(extension_path):
                        self.add_argument('--load-extension=' + extension_path)
                else:
                    raise LookupError("Extension-path doesn't exist")
