from patched_driverV1 import start_driver
driver = start_driver(mobile=True, method='cmd', pointer_as_touch=False)
driver.get('https://browserleaks.com/client-hints')
driver.quit()  # to quit Browser
