# Selenium-Profiles V2

* Overwrite **device metrics** using Selenium
* Mobile and Desktop **emulation**
* **Undetected** by Google, Cloudflare, ..
* Modifying or **adding headers** supported using "ModHeader" chrome-extension

### Feel free to test my code!

## Getting Started

### Dependencies

* [Python3](https://www.python.org/downloads/)
* Windows 10 (Linux not tested yet)
* [Chrome-Browser](https://www.google.de/chrome/) installed
* Requirements.txt

### Installing

* Download latest [chromedriver.exe](https://chromedriver.chromium.org/downloads)
* Install [Chrome-Browser](https://www.google.de/chrome/)
* ```pip install https://github.com/kaliiiiiiiiii/Selenium_Profiles/archive/refs/tags/v2.2.zip```

### Start Driver

```python
from selenium_profiles.driver import driver as mydriver
from selenium_profiles.profiles import profiles
from selenium.webdriver.common.by import By  # locate elements

mydriver = mydriver()
driver = mydriver.start(profiles.Windows())  # or .Android

# get url
driver.get('https://browserleaks.com/client-hints')  # test client hints

input("Press ENTER to exit: ")
driver.quit()  # Execute on the End!


```

Don't forget to execute
```driver.quit()```
in the End. Else-wise your temporary folder will get flooded! (Windows)

## Profiles

Example Profile: 
```json
{
  "device":{
      "mobile": false,
      "model": "modelName",
      "language": "de-CH,de;q=0.9",
      "touch_device": true,
      "maxtouchpoints": 5,
      "hardware_accel": false,
      "emulation": {"width": 384, "height": 700, "deviceScaleFactor": 10,
        "screenOrientation": {"type": "portraitPrimary", "angle": 0}},
      "agent_override": {
                "platform": "Win32",
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                "userAgentMetadata": {
                    "brands": [{"brand":"Google Chrome","version":"107"},
                              {"brand":"Chromium","version":"107"},
                              {"brand":"Not=A?Brand","version":"24"}],
                    "fullVersionList": [{"brand":"Google Chrome","version":"107.0.5304.88"},
                                        {"brand":"Chromium","version":"107.0.5304.88"},
                                        {"brand":"Not=A?Brand","version":"24.0.0.0"}],
                    "fullVersion": "107.0.5304.88",
                    "platform": "Windows",
                    "platformVersion": "10.0.0",
                    "architecture": "x86",
                    "model": "modelName",
                    "mobile": true,
                    "bitness": "64",
                    "wow64": false}
    }},
  "browser": {
      "sandbox": true, "inkognito": true,"headless":false, "proxy": null, "darkmode": true,
      "pointer_as_touch": false, "mobile_view":  false, "app": false, "touch_events": true,
      "window_size": {"x": 400, "y": 400}
    },
  "chromeoptions": {"arguments": ["--my-argument=value", ".."], "capabilities": [["cap_name", "cap_value"], ".."]},
  "cdp_cmd": [["name", "value"], ".."],
  "evaluate_on_new_document": "my_js_script",
  "plugins": {
      "selenium-wire": false,
      "modheader":"[{\"headers\":[{\"enabled\":true,\"name\":\"google\",\"value\":\"\\\"x\\\"\"}],\"shortTitle\":\"1\",\"title\":\"Profile 1\",\"version\":2}]",
      "stealth": false,
      "buster": false
    }
}
```

### To export a profile:

go to [https://jsconsole.com/](https://jsconsole.com/?function%20roundHalf%28num%29%20%7Breturn%20Math.round%28num*2%29/2%3B%7D%3Bfunction%20a%28elem%29/*if_exist%2C%20else%20null*/%7Bif%20%28typeof%20elem%20%21%3D%3D%20%27undefined%27%29%20%7Breturn%20elem%7D%20else%20%7Breturn%20null%7D%7D%3Bmynavigator%3D%20%7B%22wow64%22%3Aa%28navigator.userAgent%29.indexOf%28%27WOW64%27%29%3E-1%2C%22metrics%22%3A%7B%22width%22%3Aa%28screen.availWidth%29%2C%20%22height%22%3Aa%28screen.availHeight%29%2C%20%22scale_factor%22%3AroundHalf%28a%28window.devicePixelRatio%29%29%2C%20%22angle%22%3Aa%28screen.orientation.angle%29%2C%20%22orientation%22%3Aa%28screen.orientation.type%29%2C%20%22maxtouchpoints%22%3Aa%28window.navigator.maxTouchPoints%29%7D%2C%22memory%22%3Aa%28navigator.deviceMemory%29%2C%20%22language%22%3Aa%28navigator.language%29%2C%20%22platform%22%3Aa%28navigator.platform%29%2C%20%22useragent%22%3A%20a%28navigator.userAgent%29%2C%20%22useragentdata%22%3A%20a%28navigator.userAgentData%29%7D%3Bfunction%20copyToClipboard%28text%29%20%7Bwindow.prompt%28%22Copy%20to%20clipboard%3A%20Ctrl+C%2C%20Enter%22%2C%20text%29%3B%7D%3BcopyToClipboard%28JSON.stringify%28mynavigator%29%29) in your browser and copy the text.

and then run in Python:
```python
from sel_profiles.driver import navigator2profile
myprofile = navigator2profile("my_copied_text", filename='myprofile.json')
```

  

## Help

Please feel free to open an issue or fork!
```commandline
# no helper info yet
```

## Known Bugs

- click_as_touch makes automation hung

## Todo // Features

- [x] Undetected
- [x] support custom device metrics
- [x] export browser profile
- [x] Add License
- [x] installer.py script
  - [x] [buster captcha solver](https://github.com/dessant/buster) | [wontfix](https://github.com/kaliiiiiiiiii/Selenium_Profiles/issues/3)
  - [x] [modheader]((https://github.com/modheader/modheader_selenium))
  - [ ] [chromedriver](https://chromedriver.chromium.org/downloads)
    - [x] Windows
    - [ ] Jupyter
    - [ ] Linux (not tested yet!)
  - [ ] [Chrome-Browser](https://www.google.de/chrome/)s
  - [ ] requirements.txt
- [x] Selenium-Devices as installable module
- [ ] implement headless javascript [headless](https://github.com/microlinkhq/browserless/tree/master/packages/goto/src/evasions)
- [x] Mobile emulation
  - [ ] click_as touch makes code hung
- [x] default metrics
  - [x] Android
  - [x] Windows
  - [ ] IOS
  - [ ] Linux
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
  - [ ] [stealth]((https://github.com/diprajpatra/selenium-stealth))
- [ ] [audio_captcha_solver](https://github.com/najmi9/solve-recaptcha-python-selenium/blob/master/main.py)
- [ ] Add helper info
- [x] Rewrite driver.py to V2.2
- [ ] support for 
  - [x] Windows
  - [ ] Jupyter Notebook (Already prototype)
  - [ ] Linux


## Deprecated

* [Stealth method]((https://github.com/diprajpatra/selenium-stealth)) (Detected by Google)
* [Selenium-Wire](https://github.com/wkeeling/selenium-wire) (proxy, no https)
* [buster captcha solver](https://github.com/dessant/buster) | [wontfix](https://github.com/kaliiiiiiiiii/Selenium_Profiles/issues/3)

## Authors

[Aurin Aegerter](mailto:aurinliun@gmx.ch)

## Version History

* patched_driverV1
  * first version as importable file
* sel_profilesV2
  * added custom device metrics
  * change metrics while running
  * added example.json
  * added default.json metrics
    * Android
    * Windows
  * added navigator2profile, driver.get_profile()
  * added modheader (load modheader json profile)
  * put everything into folders
* googleV1 (not released yet!)
  * first version as importable file
* sel_profilesV2.2
  * installable as module (pip)

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
