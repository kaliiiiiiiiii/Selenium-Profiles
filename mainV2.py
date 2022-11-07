from utils import read_json
from patched_driverV2 import driver as mydriver

profile = read_json(filename='default.json')
profile = profile["Android"]  # yet supported: "Android", "Windows"

mydriver = mydriver()
driver = mydriver.start(profile)

driver.get('https://browserleaks.com/client-hints')
driver.get('https://nowsecure.nl/')

input("Press ENTER to exit: ")
driver.quit()  # Execute on the End!
