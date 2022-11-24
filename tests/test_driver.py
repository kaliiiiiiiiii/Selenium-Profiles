import unittest

from selenium_profiles.utils.utils import read_json
from selenium_profiles.driver import driver as mydriver
from selenium.webdriver.common.by import By  # locate elements

mydriver = mydriver()


def test_driver(choose: str, headless: bool = True, modheader: str = False):
    profile = read_json(filename='profiles\\default.json')
    # noinspection PyGlobalUndefined
    global mydriver
    testprofile = profile[choose]
    testprofile["plugins"]["modheader"] = modheader
    testprofile["browser"]["headless"] = headless
    driver = mydriver.start(testprofile)
    driver.get('https://browserleaks.com/client-hints')
    useragent = driver.find_element(By.XPATH, '//*[@id="content"]/table[1]/tbody/tr/td[2]').accessible_name
    exported_profile = mydriver.get_profile(None)
    driver.quit()
    return {"useragent": useragent, "exported_profile": exported_profile}


class Driver(unittest.TestCase):
    # noinspection PyGlobalUndefined
    def test_windows(self):
        global mydriver
        output = test_driver('Windows', headless=True)
        self.assertEqual(mydriver.profile['device']['agent_override']['userAgent'],
                         output["useragent"])  # add assertion here

    # noinspection PyGlobalUndefined
    def test_android(self):
        global mydriver
        output = test_driver('Android', headless=False, modheader='[{"headers":[{"enabled":true,"name":"google","value":"\\"x\\""}],"shortTitle":"1","title":"Profile 1","version":2}]')
        self.assertEqual(mydriver.profile['device']['agent_override']['userAgent'],
                         output["useragent"])  # add assertion here


if __name__ == '__main__':
    unittest.main()
