# Selenium-Profiles

* Overwrite **device metrics** using Selenium
* Mobile and Desktop **emulation**
* **Undetected** by Google, Cloudflare, ..
* [Modifying headers](#Modify-headers) supported using [Selenium-Interceptor](https://github.com/kaliiiiiiiiii/Selenium-Interceptor)
* [Touch Actions](#Touch_actions)
* [proxies with authentication](https://github.com/kaliiiiiiiiii/Selenium-Profiles/discussions/6#discussioncomment-4704385)
* making single [POST](https://github.com/kaliiiiiiiiii/Selenium-Profiles/discussions/11#discussioncomment-4797109), GET or other requests using `driver.requests.fetch(url, options)`  ([syntax](https://developer.mozilla.org/en-US/docs/Web/API/fetch#syntax))

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
from selenium_profiles.driver import driver as mydriver
from selenium_profiles.profiles import profiles
from selenium.webdriver.common.by import By  # locate elements

mydriver = mydriver()
driver = mydriver.start(profiles.Windows(), uc_driver=False)  # or .Android

# get url
driver.get('https://browserleaks.com/client-hints')  # test client hints

input("Press ENTER to exit: ")
driver.quit()  # Execute on the End!
```

Don't forget to execute
```driver.quit()```
in the End. Else-wise your temporary folder will get flooded! (Windows)

#### Run with Google-Colab
[Google-Colab](https://colab.research.google.com/github/kaliiiiiiiiii/Selenium-Profiles/blob/master/google-colab/selenium_profiles.ipynb) (file: google-colab/selenium_profiles.ipynb)

## Profiles

Example Profile: 
```json
{
  "options": {
    "browser": {
      "sandbox": true,
      "window_size": {"x":1024,"y":648},
      "headless": false,
      "load_images": true,
      "incognito": true,
      "app": false,
      "gpu": false,
      "proxy": null,
      "proxy_method": null
    },
      "extensions": {
          "extension_paths": [],
          "auth_proxy": {"host":"host","port":9000,"username":"user", "password":"password"}
        },
      "option_args": ["--my-arg1", "..."],
      "capabilities": [],
      "adb": false,
      "adb_package": "com.android.chrome",
      "use_running_app": true
  },
  "cdp": {
    "browser": {
      "pointer_as_touch": false,
      "darkmode": false,
      "mobile": true
    },
    "touch": true,
    "maxtouchpoints": 5,
    "cdp_args": [],
    "emulation": {"mobile":true,"width": 384, "height": 700, "deviceScaleFactor": 10,
        "screenOrientation": {"type": "portrait-primary", "angle": 0}},
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
                    "mobile": true,
                    "bitness": "",
                    "wow64": false}
    }}
}
```

### Modify-headers
```python

from selenium_interceptor.interceptor import cdp_listener

from selenium_profiles import driver as mydriver
from selenium_profiles.profiles import profiles

mydriver = mydriver()
profile = profiles.Windows()

driver = mydriver.start(profile)

cdp_listener = cdp_listener(driver=driver)
cdp_listener.specify_headers({"sec-ch-ua-platform":"Android"})
thread = cdp_listener.start_threaded(listener={"listener": cdp_listener.requests, "at_event": cdp_listener.modify_headers})

driver.get("https://modheader.com/headers?product=ModHeader")
```
Don't forget to execute
`cdp_listener.terminate_all()`

### Touch_actions

Example demonstration script
```python
from selenium_profiles.driver import driver as mydriver
from selenium_profiles.profiles import profiles

from selenium_profiles.scripts.driver_utils import actions

from selenium.webdriver.common.by import By


# Start Driver
mydriver = mydriver()
profile = profiles.Android()
driver = mydriver.start(profile, uc_driver=False)  # or .Android

# initialise touch_actions
actions = actions(driver)

driver.get("https://cps-check.com/de/multi-touch-test")

touch_box = driver.find_element(By.XPATH,'//*[@id="box"]') # Get element
location = actions.mid_location(touch_box) # get element middle location

# setup actions
action = actions.touch_action_chain()
action.pointer_action.move_to_location(location['x'],location['y'])
action.pointer_action.pointer_down()

# perform actions
action.perform()

# now you should see a touch indication point on the Website

# quit driver
input('Press ENTER to quit Driver\n')
driver.quit()
```

### To export a profile:

go to [https://js.do/kaliiiiiiiiiii/get_profile](https://js.do/kaliiiiiiiiiii/get_profile) in your browser and copy the text.

## Help

Please feel free to open an issue or fork!

## Known Bugs

- [click_as_touch makes automation hung](https://github.com/kaliiiiiiiiii/Selenium-Profiles/issues/1)
- Google-Colab currently doesn't work, but [solution](https://github.com/kaliiiiiiiiii/Selenium-Profiles/issues/10) already available ==> needs implementation

## Todo
- [ ] extensions
  - [x] fix adding extensions https://github.com/kaliiiiiiiiii/Selenium-Profiles/issues/15
  - [ ] add optional argument (temporary_file_path) for proxy_auth in case of permission issues (and error-handling)
- [ ] installer.py script
  - [ ] bump to [webdriver-manager](https://pypi.org/project/webdriver-manager/)
  - [ ] [Chrome-Browser](https://www.google.de/chrome/) (silent install)
- [ ] implement headless javascript [headless](https://github.com/microlinkhq/browserless/tree/master/packages/goto/src/evasions)
- [ ] js-undetectability
  - [ ] `navigator.connection`
  - [ ] `window.chrome` (for headless)
  - [x] [`navigator.maxTouchPoints`](https://github.com/kaliiiiiiiiii/Selenium-Profiles/blob/80fb6d00f246f1e6f72145ac04e04b1854e2dbbf/src/selenium_profiles/scripts/profiles.py#L256)
  - [ ] [`window.Notification`](https://github.com/microlinkhq/browserless/blob/master/packages/goto/src/evasions/navigator-permissions.js) permission (for headless)
  - [x] [`navigator.webdriver`](https://github.com/kaliiiiiiiiii/Selenium-Profiles/blob/master/src/selenium_profiles/scripts/undetected.py#L13)
  - [x] [cdc_properties](https://github.com/kaliiiiiiiiii/Selenium-Profiles/blob/master/src/selenium_profiles/scripts/undetected.py#L22)
    - [ ] maybe move to patch_chromedriver like in `uc` ? ?
  - [x] [isUserActive, isScreenUnlocked](https://github.com/kaliiiiiiiiii/Selenium-Profiles/blob/master/src/selenium_profiles/scripts/undetected.py#L16)
    - [ ] creep-js
      - [ ] `navigator.defineproperty()` lie [resource](https://github.com/abrahamjuliot/creepjs/issues/147)
        - [ ] `navigator.platform`
        - [ ] `navigator.maxTouchPoints`
      - [ ] navigator missing properties 
        - [createHandwritingRecognizer, queryHandwritingRecognizer](https://wicg.github.io/handwriting-recognition)
        - [devicePosture](https://www.w3.org/TR/device-posture/#the-deviceposture-interface)
        - [ml](https://www.w3.org/TR/webnn/#api-navigator-ml)
        - [storageBuckets](https://wicg.github.io/storage-buckets/explainer.html#setting-up-buckets)
      - [ ] [mime-types](https://github.com/microlinkhq/browserless/blob/master/packages/goto/src/evasions/media-codecs.js)
        - is: `["application/pdf","text/pdf"]`
        - should: `["application/pdf","application/x-google-chrome-pdf","application/x-nacl","application/x-pnacl"]`
      - [ ] `ambient-light-sensor` should be granted by default
      - [ ] with wrong version (is:111, emulate:107)
        - [ ] Navigator.userAgent:
          - does not match worker scope
          - v107 failed CSS features by 2 versions
          - v107 failed v109 Window features
          - v107 failed v109 CSS features
- [x] Mobile emulation
  - [ ] click_as touch makes code hung
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
      - [x] Android
- [ ] [audio_captcha_solver](https://github.com/najmi9/solve-recaptcha-python-selenium/blob/master/main.py)
- [ ] support for 
  - [x] Windows
  - [x] Jupyter Notebook (Google-Colab)
  - [x] Linux
- [x] support [proxy with credentials](https://github.com/kaliiiiiiiiii/Selenium-Profiles/discussions/6#discussioncomment-4699978)
- [ ] add error handling for [invalid keys](https://github.com/kaliiiiiiiiii/Selenium-Profiles/discussions/6#discussioncomment-4699462) in profile


## Deprecated

* [Stealth method]((https://github.com/diprajpatra/selenium-stealth)) (Detected by Google)
* [Selenium-Wire](https://github.com/wkeeling/selenium-wire) (proxy, no https)
* [buster captcha solver](https://github.com/dessant/buster) | [wontfix](https://github.com/kaliiiiiiiiii/Selenium_Profiles/issues/3)
* [Modheader-Selenium](https://github.com/modheader/modheader_selenium) (Changing headers now possible without)


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
* [porxy-auth](https://github.com/Smartproxy/Selenium-proxy-authentication)
* [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager)
