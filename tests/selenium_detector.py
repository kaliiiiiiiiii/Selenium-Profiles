from selenium_profiles.webdriver import Chrome
from selenium_profiles.profiles import profiles
from selenium.webdriver.common.by import By

# Start Driver

profile = profiles.Windows()  # or .Android
driver = Chrome(profile, uc_driver=False)

def click(x,y):
    driver.execute_cdp_cmd("Input.dispatchMouseEvent",{"type":"mousePressed", "x":x, "y":y})
    driver.execute_cdp_cmd("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y})


driver.get("https://hmaker.github.io/selenium-detector/")
driver.execute_cdp_cmd("Runtime.disable",{})


driver.find_element(By.CSS_SELECTOR, '#chromedriver-token').send_keys(
    driver.execute_script('return window.token')
    )
driver.find_element(By.CSS_SELECTOR, '#chromedriver-asynctoken').send_keys(
        driver.execute_async_script('window.getAsyncToken().then(arguments[0])')
    )
driver.find_element(By.CSS_SELECTOR, '#chromedriver-test').click()
input('Test finished, check the result on the browser page.\nPress enter to exit...')
driver.quit()