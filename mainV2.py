from selenium_profiles import driver as mydriver
from selenium_profiles.profiles import profiles
from selenium.webdriver.common.by import By  # locate elements

mydriver = mydriver()
profile = profiles.Android()
driver = mydriver.start(profile, uc_driver=False)

# get url

# test undetected
# driver.get('https://datadome.co/customers-stories/toppreise-ends-web-scraping-and-content-theft-with-datadome/')
# driver.get('https://distilnetworks.com')
driver.get('https://nowsecure.nl/')

# driver.get('https://browserleaks.com/client-hints')  # test client hints
# driver.get('https://modheader.com/headers?product=ModHeader')  # test headers
# driver.get('https://2captcha.com/demo/recaptcha-v2')  # test recaptcha-V2

# input("Press ENTER to exit: ")
driver.quit()  # Execute on the End!
