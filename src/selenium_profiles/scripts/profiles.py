def to_options(profile: dict, options):
    import warnings

    mobile = profile['device']['mobile']

    size = profile["browser"]["window_size"]
    options.add_argument("--window-size=" + str(size["x"]) + "," + str(size["y"]))
    options.add_argument('--user-agent=' + profile["device"]["agent_override"]["userAgent"])

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

    return options


def exec_cdp(profile: dict, driver):
    mobile = profile['device']['mobile']

    from selenium_profiles.scripts.cdp_tools import cdp_tools
    cdp_tools = cdp_tools(driver)

    # noinspection PyUnusedLocal
    x = driver.execute_cdp_cmd('Emulation.setIdleOverride', {'isUserActive': True, 'isScreenUnlocked': True})

    # EMULATION
    cdp_tools.set_emulation(profile["device"]["emulation"], enabled=mobile)
    cdp_tools.set_useragent(profile["device"]["agent_override"])

    # TOUCH
    cdp_tools.pointer_as_touch(mobile, profile["browser"]["pointer_as_touch"])
    cdp_tools.set_touchpoints(profile["device"]["touch_device"], maxpoints=profile["device"]["maxtouchpoints"])

    # BROWSER
    cdp_tools.set_darkmode(enabled=profile["browser"]["darkmode"], mobile=mobile)

    # additional cdp_cmd commands from profile
    if len(profile["cdp_cmd"][0]) > 0:
        for args in profile["cdp_cmd"]:
            driver.execute_cdp_cmd(args[0], args[1])


def exec_js_evaluators(profile: dict, driver, cdp_tools=None):
    if cdp_tools is None:
        from selenium_profiles.scripts.cdp_tools import cdp_tools
        cdp_tools = cdp_tools(driver)

    mobile = profile['device']['mobile']

    # remove plugins when mobile
    if mobile:
        cdp_tools.define_prop_on_new_document("navigator", "plugins", [])

    # additional evaluate on new document
    if not (profile["evaluate_on_new_document"] is None):
        print('identifier for ""evaluate_on_new_document" in profile is :' + str(
            cdp_tools.evaluate_on_new_document(profile["evaluate_on_new_document"])))

    if cdp_tools is None:
        return cdp_tools.evaluate_on_document_identifiers


# convert exported "navigator" to Profile
def navigator2profile(navigator, filename=None) -> (dict or str, str):
    import json
    from selenium_profiles.utils.utils import write_json
    import traceback

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


# get profile from current driver
def get_profile(driver, filename: str = None):
    navigator = get_navigator(driver)
    return navigator2profile(navigator, filename=filename)


# get "navigator", object convertible to profile with "navigator2profile"
def get_navigator(driver):
    import traceback
    import warnings
    from selenium_profiles.utils.utils import read
    js_return_navigator = read('js/get_navigator.js')[0]  # for exporting javascript Variables
    # noinspection PyBroadException
    try:
        returnnavigator = driver.execute_script(js_return_navigator)
        return returnnavigator
    except:
        traceback.print_exc()
        warnings.warn('get_navigator.js executed incorrectly!')
