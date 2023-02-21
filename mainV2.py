import warnings

from selenium_profiles import driver as mydriver
from selenium_profiles.profiles import profiles
from selenium_interceptor.interceptor import cdp_listener
from selenium.webdriver.common.by import By  # locate elements

mydriver = mydriver()
profile = profiles.Windows()
profile["options"]["adb"] = False
profile["options"]["incognito"] = False
profile["options"]["use_running_app"] = True
#profile["options"]["browser"]["load_images"] = False
profile["options"]["browser"]["gpu"] = True

driver = mydriver.start(profile, uc_driver=False)

async def at_response(event, connection):
    session, devtools = connection.session, connection.devtools
    cdp_listener.print_event(event)
    try:
        x = await session.execute(devtools.fetch.get_response_body(event.request_id))
    except Exception as e:
        if -32000 in e.__dict__.values() or -32602 in e.__dict__.values():  # Can only get response body on requests captured after headers received. , 'Invalid InterceptionId.'
            print(e)
            x = [None,None]
        else:
            raise e

    rc_type = event.resource_type.name.upper()
    if ((rc_type == "DOCUMENT") or (rc_type == "SCRIPT") or (rc_type == "XHR") or (rc_type == "STYLESHEET") or (rc_type == "OTHER")) and x[0]:
        decoded = cdp_listener.decode_body(x[0], event)
        encoded= cdp_listener.encode_body(decoded)
        x = (encoded, x[1])
        return devtools.fetch.fulfill_request(request_id=event.request_id, response_code=event.response_status_code, body=x[0])
    else:
        return devtools.fetch.continue_response(request_id=event.request_id)

cdp_listener = cdp_listener(driver=driver)
cdp_listener.specify_headers({"sec-ch-ua-platform":"Android"})
#thread = cdp_listener.start_threaded(listener= {"listener":cdp_listener.requests,"at_event":cdp_listener.modify_headers})

# get url

from selenium_profiles.scripts.touch_actions import touch_action_chain

touch_actions = touch_action_chain(driver)

# test undetected
# driver.get('https://datadome.co/customers-stories/toppreise-ends-web-scraping-and-content-theft-with-datadome/')
#driver.get('https://distilnetworks.com')
driver.get('https://bot.sannysoft.com/')
driver.get('https://nowsecure.nl/#relax')
#driver.get('https://modheader.com/headers?product=ModHeader')  # test headers
# driver.get('https://2captcha.com/demo/recaptcha-v2')  # test recaptcha-V2

exported_profile = driver.get_profile()
cdp_listener.terminate_all()