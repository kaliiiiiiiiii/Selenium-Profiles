import warnings

from selenium_profiles import driver as mydriver
from selenium_profiles.profiles import profiles
from selenium.webdriver.common.by import By  # locate elements

mydriver = mydriver()
profile = profiles.Windows()
profile["options"]["adb"] = False
profile["options"]["incognito"] = False
profile["options"]["use_running_app"] = True
#profile["options"]["browser"]["load_images"] = False
profile["options"]["browser"]["gpu"] = True

driver = mydriver.start(profile, uc_driver=True)

from selenium_profiles.scripts.cdp_tools import cdp_listener
# get url

# test undetected
# driver.get('https://datadome.co/customers-stories/toppreise-ends-web-scraping-and-content-theft-with-datadome/')
# driver.get('https://distilnetworks.com')
#driver.get('https://nowsecure.nl/')

#driver.get('https://modheader.com/headers?product=ModHeader')  # test headers
# driver.get('https://2captcha.com/demo/recaptcha-v2')  # test recaptcha-V2

#exported_profile = driver.get_profile()

# resource: https://stackoverflow.com/questions/66227508/selenium-4-0-0-beta-1-how-add-event-listeners-in-cdp
async def all_requests(connection):
    session, devtools = connection.session, connection.devtools
    pattern = map(devtools.fetch.RequestPattern.from_json,[{"urlPattern":"*"}])
    pattern = list(pattern)
    await session.execute(devtools.fetch.enable(patterns=pattern))

    return session.listen(devtools.fetch.RequestPaused)

def continue_request(event, connection):
    print({"type":event.resource_type.to_json(),"frame_id": event.frame_id, "url": event.request.url})
    session, devtools = connection.session, connection.devtools

    headers = event.request.headers.to_json()

    my_headers = {"sec-ch-ua-platform": "Android"}
    headers.update(my_headers)
    my_headers = []
    for item in headers.items():
        my_headers.append(devtools.fetch.HeaderEntry.from_json({"name": item[0], "value": item[1]}))

    return devtools.fetch.continue_request(request_id=event.request_id, headers=my_headers)


cdp_listener = cdp_listener(driver=driver)
thread = cdp_listener.start_threaded(listeners= {
                                                "continue":{"listener":all_requests,"at_event":continue_request},
                                                 })

driver.get('https://modheader.com/headers?product=ModHeader')


print('')