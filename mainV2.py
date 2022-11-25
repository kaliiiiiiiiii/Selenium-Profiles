from selenium_profiles import driver as mydriver
from selenium_profiles.profiles import profiles
# noinspection PyUnresolvedReferences
from selenium.webdriver.common.by import By  # locate elements

mydriver = mydriver()
driver = mydriver.start(profiles.Windows())

# get url

# driver.get('https://nowsecure.nl/')  # test undetected
driver.get('https://browserleaks.com/client-hints')  # test client hints
# driver.get('https://modheader.com/headers?product=ModHeader')  # test headers
# driver.get('https://2captcha.com/demo/recaptcha-v2')  # test recaptcha-V2

input("Press ENTER to exit: ")
driver.quit()  # Execute on the End!
