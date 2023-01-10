# Selenium-Profiles V2

* Overwrite **device metrics** using Selenium
* Mobile and Desktop **emulation**
* **Undetected** by Google, Cloudflare, ..
* Modifying or **adding headers** supported with [cdp_listeners](###Change-headers)

### Feel free to test my code!

## Getting Started

### Dependencies

* [Python >= 3.7](https://www.python.org/downloads/)
* Windows or [Google-Colab](https://colab.research.google.com/) (Linux not tested yet)
* [Chrome-Browser](https://www.google.de/chrome/) installed
* selenium-profiles

### Installing

* [Windows] Install [Chrome-Browser](https://www.google.de/chrome/)
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
    "extensions": {"extension_paths": []},
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

### Change-headers
You can change the Headers in continue_request() at my_headers = {"sec-ch-ua-platform": "Android"} .
```python

from selenium_profiles.scripts.cdp_tools import cdp_listener

# driver allready initialized

async def all_requests(connection):
    session, devtools = connection.session, connection.devtools
    pattern = map(devtools.fetch.RequestPattern.from_json,[{"urlPattern":"*"}])
    pattern = list(pattern)
    await session.execute(devtools.fetch.enable(patterns=pattern))

    return session.listen(devtools.fetch.RequestPaused)

def continue_request(event, connection):
    print({"type":event.resource_type.to_json(),"frame_id": event.frame_id, "url": event.request.url})
    session, devtools = connection.session, connection.devtools

    headers = event.request.headers.to_json()

    my_headers = {"sec-ch-ua-platform": "Android"}
    headers.update(my_headers)
    my_headers = []
    for item in headers.items():
        my_headers.append(devtools.fetch.HeaderEntry.from_json({"name": item[0], "value": item[1]}))

    return devtools.fetch.continue_request(request_id=event.request_id, headers=my_headers)


cdp_listener = cdp_listener(driver=driver)
thread = cdp_listener.start_threaded(listeners= {
                                                "continue":{"listener":all_requests,"at_event":continue_request},
                                                 })
driver.get("www.example.com")
```

### To export a profile:

go to [https://js.do/kaliiiiiiiiiii/get_profile](https://js.do/kaliiiiiiiiiii/get_profile) in your browser and copy the text.

## Help

Please feel free to open an issue or fork!

## Known Bugs

- click_as_touch makes automation hung

## Todo // Features

- [x] Undetected
- [x] support custom device metrics
- [x] export browser profile
- [x] Add License
- [x] installer.py script
  - [x] [buster captcha solver](https://github.com/dessant/buster) | [wontfix](https://github.com/kaliiiiiiiiii/Selenium_Profiles/issues/3)
  - [ ] [chromedriver](https://chromedriver.chromium.org/downloads)
    - [x] Windows
    - [x] Jupyter (Google-Colab)
    - [x] Linux (not tested yet!)
  - [ ] [Chrome-Browser](https://www.google.de/chrome/)s
  - [x] requirements.txt
- [x] Selenium-Devices as installable module
- [ ] implement headless javascript [headless](https://github.com/microlinkhq/browserless/tree/master/packages/goto/src/evasions)
- [x] Mobile emulation
  - [ ] click_as touch makes code hung
- [x] default metrics
  - [x] Android
  - [x] Windows
  - [ ] IOS
  - [ ] Linux
  - [ ] Tablet
- [x] change metrics while running
  - [ ] disable emulation while running
- [ ] test.py script
  - [x] test_driver.py
    - [x] useragent, profile_export (no error)
      - [x] Windows
      - [x] Android
- [ ] plugins support
  - [ ] [selenium-wire]((https://github.com/wkeeling/selenium-wire))
  - [x] [modheader]((https://github.com/modheader/modheader_selenium))
    - [x] load modheader profile
    - [ ] add headers without profile
  - [ ] [stealth]((https://github.com/diprajpatra/selenium-stealth))
- [ ] [audio_captcha_solver](https://github.com/najmi9/solve-recaptcha-python-selenium/blob/master/main.py)
- [x] Rewrite driver.py to V2.2
- [ ] support for 
  - [x] Windows
  - [x] Jupyter Notebook (Google-Colab)
  - [ ] Linux


## Deprecated

* [Stealth method]((https://github.com/diprajpatra/selenium-stealth)) (Detected by Google)
* [Selenium-Wire](https://github.com/wkeeling/selenium-wire) (proxy, no https)
* [buster captcha solver](https://github.com/dessant/buster) | [wontfix](https://github.com/kaliiiiiiiiii/Selenium_Profiles/issues/3)
* [Undetected-Chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver) (Selenium-Webdriver should be used directly)
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
