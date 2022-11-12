# Selenium-Devices V2

* Overwrite **device metrics** using Selenium
* Mobile and Desktop **emulation**
* **Undetected** by Google, Cloudflare, ..
* Modifying or **adding headers** supported using "ModHeader" chrome-extension

## Getting Started

### Dependencies

* [Python3](https://www.python.org/downloads/)
* Windows 10 (Linux not tested yet)
* [chromedriver.exe](https://chromedriver.chromium.org/downloads) in your root directory (already in this Repository)
* [Chrome-Browser](https://www.google.de/chrome/) installed
* Requirements.txt

### Installing

* Download latest [chromedriver.exe](https://chromedriver.chromium.org/downloads)
* Install [Chrome-Browser](https://www.google.de/chrome/)
* Install Requirements```pip install -r requirements.txt```

### Start Driver

```python
from sel_profiles.utils.utils import read_json
from sel_profiles.driver import driver as mydriver

profile = read_json(filename="profiles\\default.json")
profile = profile["Android"]  # yet supported: "Android", "Windows"

mydriver = mydriver()
driver = mydriver.start(profile)

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
  "chromeoptions": {"arguments": ["--my-argument=value", ..], "capabilities": [["cap_name", "cap_value"], ..]},
  "cdp_cmd": [["name", "value"], ..],
  "evaluate_on_new_document": "my_js_script",
  "plugins": {
      "selenium-wire": false,
      "modheader":"[{\"headers\":[{\"enabled\":true,\"name\":\"google\",\"value\":\"\\\"x\\\"\"}],\"shortTitle\":\"1\",\"title\":\"Profile 1\",\"version\":2}]",
      "stealth": false,
      "buster": false
    }
}
```

to export profile:

```python
from sel_profiles.driver import navigator2profile

# noinspection PyUnresolvedReferences
navigator = execute_javascript_in_browser(
  '{"memory":navigator.deviceMemory, "language":navigator.language, "platform":navigator.platform, "useragent": navigator.userAgent, "useragentdata": navigator.userAgentData}')
self = navigator2profile(navigator, filename='myprofile.json')
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
  - [x] [buster captcha solver](https://github.com/dessant/buster)
  - [x] [modheader]((https://github.com/modheader/modheader_selenium))
  - [ ] [chromedriver](https://chromedriver.chromium.org/downloads)
    - [x] Windows
    - [ ] Jupyter
    - [ ] Linux (not tested yet!)
  - [ ] [Chrome-Browser](https://www.google.de/chrome/)
  - [ ] requirements.txt
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
  - [ ] test_google.py ("google.py" not released yet)
- [ ] plugins support
  - [ ] [selenium-wire]((https://github.com/wkeeling/selenium-wire))
  - [x] [modheader]((https://github.com/modheader/modheader_selenium))
    - [x] load modheader profile
  - [ ] [stealth]((https://github.com/diprajpatra/selenium-stealth))
  - [x] [buster captcha solver](https://github.com/teal33t/captcha_bypass/blob/master/buster_captcha_solver_for_humans-0.7.2-an%2Bfx.xpi)
    - [ ] how to click on closed shadow-root "solve captcha" element?. 
- [ ] Add helper info
- [ ] support for 
  - [x] Windows
  - [ ] Jupyter Notebook (Already prototype)
  - [ ] Linux


## Deprecated

* [Stealth method]((https://github.com/diprajpatra/selenium-stealth)) (Detected by Google)
* [Selenium-Wire](https://github.com/wkeeling/selenium-wire) (proxy, no https)

## Authors

[Aurin Aegerter](mailto:aurin.aegerter@stud.gymthun.ch)

## Version History

* patched_driverV1
  * first version as importable file
* sel_profiles
  * added custom device metrics
  * change metrics while running
  * added example.json
  * added default.json metrics
    * Android
    * Windows
  * added navigator2profile, driver.get_profile()
  * added modheader (load modheader json profile)
  * added buster captcha solver (but can't click on "solve-captcha" yet)
  * put everything into folders
* googleV1 (not released yet!)
  * first version as importable file

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
* [README-Template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)
* [headless_js](https://github.com/microlinkhq/browserless/tree/master/packages/goto/src/evasions)
* [Selenium-Stealth](https://github.com/diprajpatra/selenium-stealth)
* [Undetected-Chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)
* [Selenium-Wire](https://github.com/wkeeling/selenium-wire)
* [Modheader-Selenium](https://github.com/modheader/modheader_selenium)
* [ModHeader docs](https://docs.modheader.com/advanced/selenium-webdriver)
* [buster captcha solver](https://github.com/dessant/buster)
* [Chromedriver-Options List](https://peter.sh/experiments/chromium-command-line-switches/)
* [Chrome DevTools Protocol (cdp_cmd)](https://chromedevtools.github.io/devtools-protocol/1-3/)
