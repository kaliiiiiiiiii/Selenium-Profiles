# Selenium-Devices V2

Undetected Chromedriver

### Chrome Browser for Web Automation

Using the [Selenium](https://github.com/SeleniumHQ/selenium) library for multiple supported device profiles.

## Getting Started

### Dependencies

* Python3
* Windows 10
* [chromedriver.exe](https://chromedriver.chromium.org/downloads) in your root directory
* [Chrome-Browser](https://www.google.de/chrome/) installed
* Requirements.txt

If you want to use ModHeader Chrome Extension:
* [modheader.crx](https://github.com/modheader/modheader_selenium/blob/main/chrome-modheader/modheader.crx) in your root directory

### Installing

* Download latest [chromedriver.exe](https://chromedriver.chromium.org/downloads)
* Install [Chrome-Browser](https://www.google.de/chrome/)
* Install Requirements```pip install -r requirements.txt```

### Start Driver

```
from utils import read_json
from patched_driverV2 import driver as mydriver

self = read_json(filename='default.json')
self = self["Windows"]  # yet supported: "Android", "Windows"

mydriver = mydriver()
driver = mydriver.start(self)

driver.get('https://browserleaks.com/client-hints')
```

Don't forget to execute
```driver.quit()```
in the End. Else-wise your temporary folder will be flooded! (Windows)

## Google-tools

```
from googleV1 import google

google = google(driver)
google.start_page()
```

## Profiles

Example Profile: 
```
{
  "device":{
      "mobile": false,
      "model": "",
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
                    "model": "",
                    "mobile": true,
                    "bitness": "64",
                    "wow64": false}
    }},
  "browser": {
      "sandbox": true, "inkognito": true, "proxy": null, "darkmode": true,
      "pointer_as_touch": false, "mobile_view":  false, "app": false, "touch_events": true,
      "window_size": {"x": 400, "y": 400}
    },
  "chromeoptions": {"arguments": [], "capabilities": []},
  "cdp_cmd": [],
  "plugins": {
      "selenium-wire": false,
      "modheader":false,
      "stealth": false
    }
}
```

to export profile:
  ```
  from patched_driverV2 import navigator2profile
  
  navigator = execute_javascript_in_browser({"memory":navigator.deviceMemory, "language":navigator.language, "platform":navigator.platform, "useragent": navigator.userAgent, "useragentdata": navigator.userAgentData} )
  self = navigator2profile(navigator, filename='myprofile.json)
  ```

  

## Help

Any advise for common problems or issues.
```
# no helper info yet
```

## Known Bugs

- click_as_touch makes code hung

## Todo // Features

- [x] Undetected
- [x] support custom device metrics
- [x] export browser profile
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
  - [ ] test_google.py
- [ ] plugins support
- [ ] Add helper info
- [ ] Add License
- [ ] support for Jupyter Notebook
- [ ] installer.py script


## Deprecated

* [Stealth method]((https://github.com/diprajpatra/selenium-stealth)) (Detected by Google)
* [Selenium-Wire](https://github.com/wkeeling/selenium-wire) (proxy, no https)

## Authors

[Aurin Aegerter](mailto:aurin.aegerter@stud.gymthun.ch)

## Version History

* patched_driverV1
  * first version as importable file
* patched_driverV2
  * added custom device metrics
  * change metrics while running
  * added example.json
  * added default.json metrics
    * Android
    * Windows
  * added navigator2profile, driver.get_profile()
  * 
* googleV1
  * first version as importable file

## License

Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

## Acknowledgments

Inspiration, code snippets, etc.
* [README-Template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)
* [Selenium_Stealth](https://github.com/diprajpatra/selenium-stealth)
* [Undetected-Chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)
* [Selenium-Wire](https://github.com/wkeeling/selenium-wire)
* [Webdriver-Options List](https://peter.sh/experiments/chromium-command-line-switches/)
* [Chrome DevTools Protocol (cdp_cmd)](https://chromedevtools.github.io/devtools-protocol/1-3/)