import warnings  # Phone Number used to often warning

from selenium.webdriver.chrome.service import Service  # for ModHeader extension
# driver.execute_script("return navigator.userAgentData") ,used for debugging
from selenium_stealth import stealth  # Change javascript variables, currently just used for mobile
from webdriver_manager.chrome import ChromeDriverManager  # for ModHeader extension
from selenium.webdriver.common.action_chains import ActionChains  # Type text without specific Element

driver = 'Global'  # Global driver Variable


def start_driver(yupiter=False, mobile=True, method='cmd', language='de-CH,de;q=0.9', model='HD1913', inkognito=True,
                 proxy=None, pointer_as_touch=False, mobile_view=True, app=False, darkmode=True,
                 sandbox=True):  # function start Driver
    if mobile and ('wire' in method):
        warnings.warn('https not supported with proxy (wire-selenium)')
        import seleniumwire.undetected_chromedriver as uc
    else:
        import undetected_chromedriver as uc
    options = uc.ChromeOptions()  # selenium.webdriver options, https://peter.sh/experiments/chromium-command-line-switches/
    options.add_argument('--accept-lang=' + language)  # language Options
    if not sandbox:
        options.add_argument('--no-sandbox')
    if mobile:  # Mobile Options
        if app:
            options.add_argument('--app')  # unknown?
            options.add_argument('--app-shell-host-window-size=400x400')  # unknown?, doesn't change anything?
            options.add_argument('--force-app-mode')  # disables desktop features
            options.add_argument('--arc-availability=officially-supported')
            options.add_argument('--force-device-ownership')  # unknown?
            options.add_argument('--arc-generate-play-auto-install')
            options.add_argument('--arc-play-store-auto-update=on')
            options.add_argument('--arc-start-mode=always-start')
            options.add_argument('--touch-devices')
            options.add_argument('--enable-features=UserActivationV2')
            # options.add_argument('--enable-features=enable-nacl') #wallet-service-use-sandbox
        # options.add_argument('--as-browser')  # unknown?
        options.add_argument('--disable-gpu')  # google render, canvas fingerprint[3Win/1Android]
        options.add_argument('--override-use-software-gl-for-tests')  # google render, unique canvas fingerprint
        options.add_argument('--enable-touchview')  # unknown?
        options.add_argument('--enable-virtual-keyboard')  # unknown?
        options.add_argument(  # unknown?
            '--use-mobile-user-agent --enable-viewport --validate-input-event-stream --enable-longpress-drag-selection ' # todo does "--use-mobile-user-agent" have an effect?
            '--touch-selection-strategy=direction --disable-composited-antialiasing --enable-dom-distiller '
            ' --top-controls-show-threshold=0.5 '
            '--top-controls-hide-threshold=0.5')
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Linux; Android 11; " + model + ") AppleWebKit/537.36 (KHTML, like Gecko) "
                                                                      "Chrome/105.0.0.0 Mobile Safari/537.36")

        options.set_capability("general.useragent.override",
                               "Mozilla/5.0 (Linux; Android 11; " + model + ") AppleWebKit/537.36 (KHTML, like Gecko) "
                                                                            "Chrome/105.0.0.0 Mobile Safari/537.36")
        options.set_capability('platform', 'Android') # todo does it have an effect?
        options.add_argument("--touch-events=enabled")  # enable touch events
        if 'modheader' in method:
            warnings.warn('modheader is desperated')
            options.add_argument('--load-extension=C:/Users/aurin/PycharmProjects/Collab_bot/modheader')
        #  options.add_experimental_option('w3c', False)  # needed for TouchActions, but breaks Element properties
    if inkognito:  # use Incognito?
        if ('modheader' in method) and mobile:
            warnings.warn('"Modheader" not supported with inkognito, disabling inkognito..')
        else:
            options.add_argument("--incognito")

    # options.add_argument("--disable-extensions")  # disable extensions
    # options.add_argument("--disable-plugins")  # not working yet

    def interceptor(request):  # currently just used if Mobile
        del request.headers['User-Agent']  # Delete the headers first
        del request.headers['sec-ch-ua']
        del request.headers['sec-ch-ua-mobile']
        del request.headers['sec-ch-ua-arch']
        del request.headers['sec-ch-ua-platform']
        del request.headers['sec-ch-ua-platform-version']
        del request.headers['platformversion']
        del request.headers['sec-ch-ua-model']
        del request.headers['model']
        del request.headers['platform']
        del request.headers['ect']
        del request.headers['accept']
        del request.headers['content-disposition']
        del request.headers['sec-ch-viewport-width']
        del request.headers['viewport-width']
        del request.headers['sec-ch-viewport-height']
        del request.headers['viewport-height']
        del request.headers['sec-ch-dpr']
        del request.headers['dpr']
        request.headers[  # mobile Headers
            'User-Agent'] = 'Mozilla/5.0 (Linux; Android 11; ' + model + ') AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                                                         'Chrome/105.0.0.0 Mobile Safari/537.36 '
        request.headers['sec-ch-ua'] = '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"'
        request.headers['sec-ch-ua-mobile'] = '?1'
        #  request.headers['platform'] = '"Android"'
        request.headers['sec-ch-ua-platform'] = '"Android"'
        # request.headers['content-disposition'] = 'attachment'
        request.headers['sec-ch-ua-full-version'] = '"105.0.5195.136"'
        request.headers[
            'sec-ch-ua-full-version-list'] = '"Google Chrome",v="105.0.5195.136","Not)A;Brand";v="8.0.0.0","Chromium";v="105.0.5195.136"'
        request.headers['sec-ch-ua-platform-version'] = '"11.0.0"'
        # request.headers['sec-ch-ua-arch'] = '""'
        # request.headers['sec-ch-ua-bitness'] = '""'
        request.headers['sec-ch-ua-model'] = '"' + model + '"'
        # request.headers['sec-ch-viewport-width'] = '980'
        # request.headers['viewport-width'] = '980'
        # request.headers['sec-ch-viewport-height'] = '2123'
        # request.headers['viewport-height'] = '2123'
        request.headers['ect'] = '4g'
        # request.headers['sec-ch-dpr'] = '2.8125'
        # request.headers['dpr'] = '2.8125'
        request.headers[
            'accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,' \
                        '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9 '

    if proxy is not None:  # proxy [IP:Port], Optional Proxy Server
        options.add_argument(f'--proxy-server=socks5://' + proxy)
        print('proxy= "' + proxy + '"')

    global driver  # use global driver variable
    if mobile:
        if 'modheader' in method:
            driver = uc.Chrome(use_subprocess=True, options=options,
                               service=Service(ChromeDriverManager().install()),
                               # needed when using ModHeader extension
                               keep_alive=True)  # start undetected_chromedriver
        else:
            driver = uc.Chrome(use_subprocess=True, options=options, keep_alive=True)  # start undetected_chromedriver
    else:
        driver = uc.Chrome(use_subprocess=True, options=options)  # start undetected_chromedriver

    if mobile:  # currently just for mobile used functions
        # driver.get("chrome://extensions/?id=gaodcldehcjdaakneciebjaedgmhgiag")  # make extension allowed in  incognito
        # driver.execute_script("return document.querySelector('extensions-manager').shadowRoot.querySelector('#viewManager > extensions-detail-view.active').shadowRoot.querySelector('div#container.page-container > div.page-content > div#options-section extensions-toggle-row#allow-incognito').shadowRoot.querySelector('label#label input').click()");
        if 'wire' in method:
            driver.request_interceptor = interceptor  # selenium-wire (change headers), currently just used for mobile
        if 'modheader' in method:
            driver.get(
                'https://webdriver.modheader.com/add?User-Agent=Mozilla%2F5.0+%28Linux%3B+Android+11%3B+' + model + '%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F105.0.0.0+Mobile+Safari%2F537.36&sec-ch-ua-mobile=%3F1&sec-ch-ua-platform=%22Android%22&sec-ch-ua=%22Google+Chrome%22%3Bv%3D%22105%22%2C+%22Not%29A%3BBrand%22%3Bv%3D%228%22%2C+%22Chromium%22%3Bv%3D%22105%22&sec-ch-ua-arch=&sec-ch-ua-platform-version=&platformversion=&sec-ch-ua-model=&model=&platform=&ect=&accept=text%2Fhtml%2Capplication%2Fxhtml%2Bxml%2Capplication%2Fxml%3Bq%3D0.9%2Cimage%2Favif%2Cimage%2Fwebp%2Cimage%2Fapng%2C*%2F*%3Bq%3D0.8%2Capplication%2Fsigned-exchange%3Bv%3Db3%3Bq%3D0.9+&content-disposition=')
        if 'stealth' in method:  # gets detected by Google!
            warnings.warn('Selenium-Stealth gets detected at least by Google!')
            stealth(driver,
                    # change Javascript variables, currently just used for mobile, only works when request made automated
                    user_agent="Mozilla/5.0 (Linux; Android 11; " + model + ") AppleWebKit/537.36 (KHTML, like Gecko) "
                                                                            "Chrome/105.0.0.0 Mobile Safari/537.36",
                    vendor="Google Inc.",
                    platform='Linux aarch64',
                    webgl_vendor="Qualcomm",  # Javascript overwrite, currently just possible with stealth
                    renderer="Adreno (TM) 640",  # Javascript overwrite, currently just possible with stealth
                    fix_hairline=True,
                    webdriver='false',
                    )
        if 'cmd' in method:  # devloper mobile Emulation, https://chromedevtools.github.io/devtools-protocol/tot/Emulation/
            driver.get('https://www.google.com/')  # wait browser to start
            if mobile_view:
                warnings.warn('mobile_view makes "Native Client, internal-nacl-plugin" appear in navigator.plugins')
                driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride',
                                       # mobile view, .click() working, makes "Native Client, internal-nacl-plugin" appear in navigator.plugins
                                       {'mobile': True, "width": 384, "height": 700, "deviceScaleFactor": 10,
                                        'screenOrientation': {'type': 'portraitPrimary',
                                                              'angle': 0}})  # *height=832 in original!
                driver.execute_cdp_cmd('Page.setDeviceMetricsOverride',
                                       # mobile view, .click() working, makes "Native Client, internal-nacl-plugin" appear in navigator.plugins
                                       {'mobile': True, "width": 384, "height": 700, "deviceScaleFactor": 10,
                                        'screenOrientation': {'type': 'portraitPrimary',
                                                              'angle': 0}})  # *height=832 in original!
            if pointer_as_touch:
                warnings.warn('Actions execute, but then take long when "EmitTouchEventsForMouse"!')
                driver.execute_cdp_cmd('Emulation.setEmitTouchEventsForMouse', {'enabled': True,
                                                                                'configuration': 'mobile'})  # executes, but then takes long [maybe check if sucess?]
            if darkmode:
                if not mobile_view:
                    warnings.warn('darkmode might look weird without mobile_view!')
                driver.execute_cdp_cmd('Emulation.setAutoDarkModeOverride',
                                       {'enabled': True})  # darkmode, might look weird:/
            driver.execute_cdp_cmd('Emulation.setIdleOverride',
                                   {'isUserActive': True, 'isScreenUnlocked': True})  # .click() working
            driver.execute_cdp_cmd('Emulation.setTouchEmulationEnabled',
                                   {'enabled': True, 'maxTouchPoints': 5})  # allready set in options
            driver.execute_cdp_cmd('Emulation.setUserAgentOverride', {  # .click() working
                'platform': 'Linux aarch64',
                'userAgent': "Mozilla/5.0 (Linux; Android 11; " + model + ") AppleWebKit/537.36 (KHTML, like Gecko) ""Chrome/105.0.0.0 Mobile Safari/537.36",
                'userAgentMetadata': {
                    'brands': [{"brand": "Google Chrome", "version": "105"}, {"brand": "Not)A;Brand", "version": "8"},
                               {"brand": "Chromium", "version": "105"}],
                    'fullVersionList': [{"brand": "Google Chrome", "version": "105.0.5195.136"},
                                        {"brand": "Not)A;Brand", "version": "8.0.0.0"},
                                        {"brand": "Chromium", "version": "105.0.5195.136"}],
                    'fullVersion': '105.0.5195.136',
                    'platform': 'Android',
                    'platformVersion': '11.0.0',
                    'architecture': '',
                    'model': model,
                    'mobile': True,
                    'bitness': '',
                    'wow64': False}
            })
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {  # .click() working
                'platform': 'Linux aarch64',
                'userAgent': "Mozilla/5.0 (Linux; Android 11; " + model + ") AppleWebKit/537.36 (KHTML, like Gecko) ""Chrome/105.0.0.0 Mobile Safari/537.36",
                'userAgentMetadata': {
                    'brands': [{"brand": "Google Chrome", "version": "105"}, {"brand": "Not)A;Brand", "version": "8"},
                               {"brand": "Chromium", "version": "105"}],
                    'fullVersionList': [{"brand": "Google Chrome", "version": "105.0.5195.136"},
                                        {"brand": "Not)A;Brand", "version": "8.0.0.0"},
                                        {"brand": "Chromium", "version": "105.0.5195.136"}],
                    'fullVersion': '105.0.5195.136',
                    'platform': 'Android',
                    'platformVersion': '11.0.0',
                    'architecture': '',
                    'model': model,
                    'mobile': True,
                    'bitness': '',
                    'wow64': False}
            })
    # global driver
    return driver


def sendkeys(driver, keys):  # send keys without specific Element
    actions = ActionChains(driver)
    actions.send_keys(str(keys))
    actions.perform()
