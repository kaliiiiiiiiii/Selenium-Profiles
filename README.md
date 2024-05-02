# Selenium-Profiles

[![Downloads](https://static.pepy.tech/badge/selenium-profiles)](https://pepy.tech/project/selenium-profiles) [![](https://img.shields.io/pypi/v/selenium-profiles.svg?color=3399EE)](https://pypi.org/project/selenium-profiles/)

* Overwrite **device metrics** using Selenium
* Mobile and Desktop **emulation**
* **Undetected** by Google, Cloudflare, creep-js using [selenium-driverless](#selenium-driverless)
* [Modifying headers](#Modify-headers) supported using [Selenium-Interceptor](https://github.com/kaliiiiiiiiii/Selenium-Interceptor) or seleniumwire
* [Touch Actions](#Touch_actions)
* dynamic proxies with authentication
* making single [POST](https://github.com/kaliiiiiiiiii/Selenium-Profiles/discussions/11#discussioncomment-4797109), GET or other requests using `driver.profiles.fetch(url)`  ([syntax](https://developer.mozilla.org/en-US/docs/Web/API/fetch#syntax))
* headless unofficially supported
* apply profile on already running driver with `driver.profiles.apply(profiles.Android())`
* use of [seleniumwire](https://github.com/wkeeling/selenium-wire)

## Sponsors

### [Capsolver](https://is.gd/OJSVP4)

<a href="https://is.gd/OJSVP4" >
  <img src="https://github.com/kaliiiiiiiiii/Selenium-Driverless/blob/master/assets/capsolver.png" alt="drawing" width="60%"/>
</a>

An AI-powered captcha-solver service.

for the latest features, have a look at the `dev` branch

### Feel free to test my code!

## Getting Started

### Dependencies

* [Python >= 3.7](https://www.python.org/downloads/)
* [Chrome-Browser](https://www.google.de/chrome/) installed

### Installing

* Install [Google-Chrome](https://www.google.de/chrome/) (or another chromium-based browser)
* ```pip install selenium-profiles```

### Start Driver

```python
from selenium_profiles.webdriver import Chrome
from selenium_profiles.profiles import profiles
from selenium.webdriver.common.by import By  # locate elements
from seleniumwire import webdriver


profile = profiles.Windows() # or .Android
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = Chrome(profile, options=options,
                uc_driver=False
                )

# get url
driver.get('https://abrahamjuliot.github.io/creepjs/')  # test fingerprint

input("Press ENTER to exit: ")
driver.quit()  # Execute on the End!
```

Don't forget to execute
```driver.quit()```
in the End. Else-wise your temporary folder will get flooded!

#### Run with Google-Colab
__[Google-Colab](https://colab.research.google.com/github/kaliiiiiiiiii/Selenium-Profiles/blob/master/google-colab/selenium_profiles.ipynb) (file: master@google-colab/selenium_profiles.ipynb)__

## Profiles

Example Profile: 
```python
profile = \
{
  "options": {
      "sandbox": True,
      "headless": False,
      "load_images": True,
      "incognito": True,
      "touch": True,
      "app": False,
      "gpu": False,
      "proxy": "http://example-proxy.com:9000", # note: auth not supported,
      "extension_paths": ["path/to/extension_1", ...], # directory, .crx or .zip
      "args": ["--my-arg1", ...],
      "capabilities": {"cap_1":"val_1", "cap_2":"val_2"},
      "experimental_options":{"option1":"value1", "option2":"value2"},
      "adb": False, # run on harware device over ADB
      "adb_package": "com.android.chrome",
      "use_running_app": True
  },
  "cdp": {
    "touch": True,
    "darkmode":None,
    "maxtouchpoints": 5,
    "cores":8,
    "cdp_args": [],
    "emulation": {"mobile":True,"width": 384, "height": 700, "deviceScaleFactor": 10,
        "screenOrientation": {"type": "portrait-primary", "angle": 0}},
    "patch_version": True, # to patch automatically, or use "111.0.5563.111"
    "useragent": {
                "platform": "Linux aarch64",
                "acceptLanguage":"en-US",
                "userAgent": "Mozilla/5.0 (Linux; Android 11; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36",
                "userAgentMetadata": {
                    "brands": [{"brand": "Google Chrome", "version": "105"}, {"brand": "Not)A;Brand", "version": "8"},
                               {"brand": "Chromium", "version": "105"}],
                    "fullVersionList": [{"brand": "Google Chrome", "version": "105.0.5195.136"},
                                        {"brand": "Not)A;Brand", "version": "8.0.0.0"},
                                        {"brand": "Chromium", "version": "105.0.5195.136"}],
                    "fullVersion": "105.0.5195.136",
                    "platform": "Android",
                    "platformVersion": "11.0.0",
                    "architecture": "",
                    "model": "HD1913",
                    "mobile": True,
                    "bitness": "",
                    "wow64": False}
    }
  },
"proxy":{
  "proxy":"socks5://user1:pass@example_jost.com:5001", 
  "bypass_list":["localhost"]
  }
}
```

### selenium-driverless
warning: 
- this package is experimental and might include bugs, please report them at [bug-reports](https://github.com/kaliiiiiiiiii/Selenium-Driverless/issues)
- might only work with 64-bit Python installations
- profiles might make it detected
- requires `pip install selenium-driverless>=1.3.4` first
```python
from selenium_profiles.webdriver import Chrome
from selenium_profiles.profiles import profiles
from selenium_driverless.webdriver import ChromeOptions
from selenium_driverless.types.by import By

profile = profiles.Windows()  # or .Android
options = ChromeOptions()
# options.add_argument("--headless=new")
driver = Chrome(profile, options=options, driverless_options=True)

# get url
driver.get('https://nowsecure.nl#relax')  # test fingerprint

driver.quit()  # Execute on the End!
```
see [documentation](https://github.com/kaliiiiiiiiii/Selenium-Driverless) for usages


### Modify-headers

using selenium-wire
```python
from selenium_profiles import webdriver
from selenium_profiles.profiles import profiles

profile = profiles.Android()

driver = webdriver.Chrome(profile, uc_driver=False, seleniumwire_options=True) # or pass seleniumwire-options

def interceptor(request):
    request.headers['New-Header'] = 'Some Value'
driver.request_interceptor = interceptor

# checkout headers
driver.get("https://httpbin.org/headers")

input("Press ENTER to quit..")
driver.quit()
exit()
```

Using [Selenium-Injector](https://github.com/kaliiiiiiiiii/Selenium-Injector)
```python
from selenium_profiles.webdriver import Chrome

driver = Chrome(injector_options=True)
injector = driver.profiles.injector

# modify headers
injector.declarativeNetRequest.update_headers({"test": "test_2", "sec-ch-ua-platform": "Android"})
rules = injector.declarativeNetRequest.dynamic_rules
headers = injector.declarativeNetRequest._headers

driver.get("https://httpbin.org/headers")
input("press ENTER to continue")

# block images
injector.declarativeNetRequest.update_block_on(resource_types=["image"])

driver.get("https://www.wikimedia.org/")

input("press ENTER to exit")
driver.quit()
```

### Touch_actions

Example demonstration script
```python
from selenium_profiles.webdriver import Chrome
from selenium_profiles.profiles import profiles
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions

from selenium_profiles.scripts.driver_utils import TouchActionChain


# Start Driver
options = ChromeOptions()
profile = profiles.Android() # or .Windows()

driver = Chrome(profile, uc_driver=False, options=options)

# initialise touch_actions
chain = TouchActionChain(driver)

driver.get("https://cps-check.com/de/multi-touch-test")

touch_box = driver.find_element(By.XPATH,'//*[@id="box"]') # Get element



chain.touch_and_hold(touch_box)
chain.pause(10)
chain.release(touch_box)

# perform actions
chain.perform()

# now you should see a touch indication
# point on the Website for 10 seconds

# quit driver
input('Press ENTER to quit Driver\n')
driver.quit()
```

### connect to running driver
Undetectability isn't garanteed
```python
from selenium import  webdriver
driver = webdriver.Chrome()
# driver allready started:)


from selenium_profiles.webdriver import profiles as profile_manager
from selenium_profiles.profiles import profiles

profile = profiles.Android() # or .Android()
driver.profiles = profile_manager(driver=driver, profile=profile)
driver.profiles.apply(profile)

driver.get('https://hmaker.github.io/selenium-detector/')  # test fingerprint

input("Press ENTER to exit")
driver.quit()  # Execute on the End!
```

### Set proxies dynamically or with options
```python
from selenium_profiles.webdriver import Chrome
from selenium_profiles.profiles import profiles

profile = profiles.Windows() # or .Android()
profile["proxy"] = {
  "proxy":"http://user1:pass1@example_host.com:41149"
  }

driver = Chrome(profile=profile, injector_options=True)

driver.profiles.proxy.set_single("http://user2:pass2@example_host.com:41149")
print(driver.profiles.proxy.proxy)

driver.quit()  # Execute on the End!
```

### To export a profile:

go to [https://js.do/kaliiiiiiiiiii/get_profile](https://js.do/kaliiiiiiiiiii/get_profile) in your browser and copy the text.

## Help

Please feel free to open an issue or fork!

## Known Bugs

- [click_as_touch makes automation hung](https://github.com/kaliiiiiiiiii/Selenium-Profiles/issues/1)


## Todo
- [x] js-undetectability
  - [ ] [`navigator.connection`]
  - [ ] fonts don't match platform
  - [ ] does not match worker scope (Emulation) [crbug#1358491](https://bugs.chromium.org/p/chromium/issues/detail?id=1358491)
    - `Navigator.userAgent`
    - `Navigator.platform`
    - `navigator.hardwareConcurrency`
  - [ ] emulation leak on new tabs [diskussion](https://github.com/kaliiiiiiiiii/Selenium-Profiles/discussions/50)
  - [ ] [selenium-detector](https://github.com/HMaker/HMaker.github.io/blob/master/selenium-detector/chromedriver.js)
    - [ ] Either Devtools Console is open or CDP Runtime Domain is enabled => patch javascript objects using a Proxy or disable CDP.Runtime domain?
    - [ ] [document.$cdc_asdjflasutopfhvcZLmcfl_](https://source.chromium.org/chromium/chromium/src/+/main:chrome/test/chromedriver/js/call_function.js;l=219)
    - [ ] [`document.$chrome_asyncScriptInfo`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/test/chromedriver/chrome/web_view_impl.cc;l=1586-1597;drc=2e14a3ac178ee87aa9154e5a15dcd986af1b6059)
    - [ ] driver.execute_script() usage (needs hook on called element)
    - [ ] driver.execute_async_script() usage (needs hook on called element)
    - [ ] driver.find_element() usage
    - [x] [`window.cdc_adoQpoasnfa76pfcZLmcfl`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/test/chromedriver/chrome/devtools_client_impl.cc;l=526-532;drc=f915006bb8e09e0c29016cf9ab9e737cdebc1adc)
- [x] default metrics
  - [x] Android
  - [x] Windows
  - [ ] IOS
  - [ ] Linux
  - [ ] Tablet
- [ ] test.py script
  - [x] test_driver.py
    - [x] assert useragent, profile_export (no error)
      - [x] Windows
        - [x] useragent-data
        - [ ] undetected
          - [ ] headless
      - [x] Android
       - [x] useragent-data
       - [ ] undetected
         - [ ] headless


## Deprecated

* [Stealth method]((https://github.com/diprajpatra/selenium-stealth)) (Detected by Google)
* [buster captcha solver](https://github.com/dessant/buster) | [wontfix](https://github.com/kaliiiiiiiiii/Selenium_Profiles/issues/3)


## Authors

[Aurin Aegerter](mailto:aurinliun@gmx.ch)

## License

Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

## Disclaimer

I am not responsible what you use the code for!!! Also no warranty!

## Acknowledgments

Inspiration, code snippets, etc.

* [Selenium](https://github.com/SeleniumHQ/selenium)
* [selenium-documentation](https://www.selenium.dev/documentation/)
* [README-Template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)
* [headless_js](https://github.com/microlinkhq/browserless/tree/master/packages/goto/src/evasions)
* [Selenium-Stealth](https://github.com/diprajpatra/selenium-stealth)
* [Undetected-Chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)
* [Selenium-Wire](https://github.com/wkeeling/selenium-wire)
* [Modheader-Selenium](https://github.com/modheader/modheader_selenium)
* [ModHeader docs](https://docs.modheader.com/advanced/selenium-webdriver)
* [buster captcha solver](https://github.com/dessant/buster) | [wontfix](https://github.com/kaliiiiiiiiii/Selenium-Profiles/issues/3)
* [audio_captcha_solver](https://github.com/najmi9/solve-recaptcha-python-selenium/blob/master/main.py)
* [Chromedriver-Options List](https://peter.sh/experiments/chromium-command-line-switches/)
* [Chrome DevTools Protocol (cdp_cmd)](https://chromedevtools.github.io/devtools-protocol/1-3/)
* [example_pypi_package](https://github.com/tomchen/example_pypi_package)
* [google-colab installer](https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/108)
* [scripts/touch_action_chain](https://www.reddit.com/r/Appium/comments/rbx1r2/touchaction_deprecated_please_use_w3c_i_stead/)
* [cdp_event_listeners](https://stackoverflow.com/questions/66227508/selenium-4-0-0-beta-1-how-add-event-listeners-in-cdp)
* [proxy-auth](https://github.com/Smartproxy/Selenium-proxy-authentication)
* [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager)
* [dynamic subclasses](https://stackoverflow.com/a/9270908/20443541)
