from utils import read_json
from patched_driverV2 import driver as mydriver
from selenium.webdriver.common.by import By  # locate elements

profile = read_json(filename='default.json')
profile = profile["Android"]  # yet supported: "Android", "Windows"

mydriver = mydriver()
driver = mydriver.start(profile)

# get url

# driver.get('https://nowsecure.nl/')  # test undetected
driver.get('https://browserleaks.com/client-hints')  # test client hints
# driver.get('https://modheader.com/headers?product=ModHeader')  # test headers
# driver.get('https://2captcha.com/demo/recaptcha-v2')  # test recaptcha-V2

input("Press ENTER to exit: ")
driver.quit()  # Execute on the End!
