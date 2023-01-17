import unittest

from selenium_profiles.utils.utils import read_json
from selenium_profiles.driver import driver as mydriver
from selenium.webdriver.common.by import By  # locate elements

mydriver = mydriver()


def test_driver(choose: str, headless: bool = True, uc_driver=False):
    import json
    profile = read_json(filename='profiles\\default.json')
    # noinspection PyGlobalUndefined
    global mydriver
    testprofile = profile[choose]
    testprofile["options"]["browser"]["headless"] = headless
    driver = mydriver.start(testprofile, uc_driver=uc_driver)
    driver.get('https://browserleaks.com/client-hints')
    useragent = driver.find_element(By.XPATH, '//*[@id="content"]/table[1]/tbody/tr/td[2]').accessible_name
    exported_profile = driver.get_profile()
    driver.quit()

    del driver.profile["cdp"]["useragent"]['acceptLanguage'] # get_profile doesn't include 'acceptLanguage' yet!

    print(choose+'\n'+useragent+'\n')
    return {"profile": driver.profile, "exported_profile": exported_profile, "useragent":useragent}


class Driver(unittest.TestCase):
    # noinspection PyGlobalUndefined
    # Hello World!
    def test_windows(self):
        global mydriver
        output = test_driver('Windows', headless=True)
        self.assertEqual(output["exported_profile"]["cdp"]["useragent"],
                         output["profile"]["cdp"]["useragent"])  # add assertion here

    # noinspection PyGlobalUndefined
    def test_android(self):
        global mydriver
        output = test_driver('Android', headless=False)
        self.assertEqual(output["exported_profile"]["cdp"]["useragent"],
                         output["profile"]["cdp"]["useragent"])  # add assertion here


if __name__ == '__main__':
    unittest.main()
