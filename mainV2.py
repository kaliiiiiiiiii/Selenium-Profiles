from utils import read_json
from patched_driverV2 import driver as mydriver
from googleV1 import google

profile = read_json(filename='default.json')
profile = profile["Windows"]

mydriver = mydriver()
driver = mydriver.start(profile)

google = google(driver)
#google.start_page()

driver.get('https://browserleaks.com/client-hints')
#navigator = mydriver.get_navigator()
driver.quit()