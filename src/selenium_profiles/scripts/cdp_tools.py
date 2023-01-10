from typing import Dict, List  # define types in functions
import warnings
import json
import traceback


# noinspection PyPep8Naming
class cdp_tools(object):
    def __init__(self, driver):
        self.driver = driver

        # initial property
        self.evaluate_on_document_identifiers = {}

    # EMULATION

    def set_emulation(self, emulation:bool or None) -> (Dict[str, int or Dict[str, str or int or float]]):
        if emulation:
            warnings.warn('disabling emulation not supported')
            return self.driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', emulation)

    def clear_emulation(self, enabled:bool or None):
        if enabled or (enabled is None):
            self.driver.execute_cdp_cmd("Emulation.clearDeviceMetricsOverride", {})

    def set_useragent(self, useragent) -> Dict[str, str or Dict[str, str or bool or List[Dict[str, str]]]] or None:
        return self.driver.execute_cdp_cmd('Emulation.setUserAgentOverride', useragent)

    # BROWSER

    def set_darkmode(self, enabled=True, mobile=True) -> (bool, bool):
        if not (mobile or mobile is None) and enabled:
            warnings.warn('darkmode might look weird without mobile_view!')
        if enabled:
            return self.driver.execute_cdp_cmd('Emulation.setAutoDarkModeOverride',
                                           {'enabled': enabled})

    # TOUCH

    def set_touchpoints(self, enabled:bool or None=True, maxpoints:int or None=10):  # set touch options
        if maxpoints is None:
            maxpoints = 10
        return self.driver.execute_cdp_cmd('Emulation.setTouchEmulationEnabled',
                                           {'enabled': enabled, 'maxTouchPoints': maxpoints})  # already set in options

    def pointer_as_touch(self, mobile:bool or None, enabled:bool or None=True):  # (makes code hung)
        if mobile or mobile is None:
            config = 'mobile'
        else:
            config = 'desktop'
        if enabled:
            warnings.warn('Actions execute, but then take long when "EmitTouchEventsForMouse"!')
            return self.driver.execute_cdp_cmd('Emulation.setEmitTouchEventsForMouse', {'enabled': enabled,
                                                                                    'configuration': config})  # executes, but then takes long [maybe check if success?]

    # OVERRIDE JAVASCRIPT

    def evaluate_on_new_document(self, js: str):  # evaluate js on every new page
        identifier = int(
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})["identifier"])
        self.evaluate_on_document_identifiers.update({identifier: js})
        return identifier

    # remove js evaluation  on every new page for specific script
    def remove_evaluate_on_document(self, identifier: int):
        del self.evaluate_on_document_identifiers[identifier]
        return self.driver.execute_cdp_cmd("Page.removeScriptToEvaluateOnNewDocument", {"identifier": str(identifier)})

    # define var.property for javascript
    def define_prop_on_new_document(self, var, prop, val, func='get: ()') -> (str, str, any, str):
        self.evaluate_on_new_document(
            "Object.defineProperty(" + var + ", " + json.dumps(prop) + ", {" + func + " => " + json.dumps(val) + "})")

    # COOKIES

    def get_cookies(self):
        return self.driver.execute_cdp_cmd("Network.getAllCookies", {})

    def get_cookie(self, urls: list = None):
        if urls:
            arg = {"urls": urls}
        else:
            arg = {}
        return self.driver.execute_cdp_cmd("Network.getCookies", arg)

    def add_cookie(self, cookie_dict):
        return self.driver.execute_cdp_cmd("Network.setCookie", cookie_dict)

    def delete_cookie(self, name: str):
        return self.driver.execute_cdp_cmd("Network.deleteCookies", {"name": name})

    def delete_all_cookies(self):
        return self.driver.execute_cdp_cmd("Network.clearBrowserCookies", {})

class cdp_listener(object):
    from typing import Dict

    def __init__(self, driver):
        self.listeners = {}
        self.driver = driver
        self.my_headers= None
        self.print_requests = True
    async def async_helper(self):
        async with self.driver.bidi_connection() as connection:
            session, devtools = connection.session, connection.devtools

            for listener in self.listeners.items():
                my_listener = await listener[1]["listener"](connection=connection)

                async for event in my_listener:
                    try:
                        await session.execute(listener[1]["at_event"](event=event, connection=connection))
                    except Exception as e:
                        traceback.print_exception(e)

    def trio_helper(self):
        import trio
        trio.run(self.async_helper)

    def start_threaded(self, listeners: Dict[str,Dict[callable, callable]] = {}):
        if listeners:
            self.listeners = listeners

        import threading
        thread = threading.Thread(target=self.trio_helper)
        thread.start()
        return thread

    def add_listeners(self, listeners: Dict[str,Dict[callable, callable]]):
        self.listeners = listeners

    def remove_listener(self, listener:str):
        del self.listeners[listener]

    def connection_refused(self,event, connection):
        self.print_request(event)

        session, devtools = connection.session, connection.devtools
        # show_image(event.request.url)
        return devtools.fetch.fail_request(request_id=event.request_id,
                                           error_reason=devtools.network.ErrorReason.CONNECTION_REFUSED)

    def modify_headers(self, event, connection):
        self.print_request(event)

        session, devtools = connection.session, connection.devtools

        headers = event.request.headers.to_json()

        try:
            headers.update(self.my_headers)
        except TypeError as e:
            traceback.print_exception(e)
            raise TypeError("Define headers using cdp_listener.specify_headers.\n")
        my_headers = []
        for item in headers.items():
            if item[1]: # if value is set
                my_headers.append(devtools.fetch.HeaderEntry.from_json({"name": item[0], "value": item[1]}))

        return devtools.fetch.continue_request(request_id=event.request_id, headers=my_headers)

    def specify_headers(self, headers:Dict[str, str]):
        self.my_headers = headers

    async def all_images(self, connection):
        session, devtools = connection.session, connection.devtools
        pattern = map(devtools.fetch.RequestPattern.from_json, [{"resourceType": "Image"}])
        pattern = list(pattern)
        await session.execute(devtools.fetch.enable(patterns=pattern))

        return session.listen(devtools.fetch.RequestPaused)

    async def all_requests(self, connection):
        session, devtools = connection.session, connection.devtools
        pattern = map(devtools.fetch.RequestPattern.from_json, [{"urlPattern": "*"}])
        pattern = list(pattern)
        await session.execute(devtools.fetch.enable(patterns=pattern))

        return session.listen(devtools.fetch.RequestPaused)

    def show_image(self, url: str):  # show image from URL
        from PIL import Image
        from io import BytesIO
        import requests
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img.show()
        except Exception as e:
            traceback.print_exception(e)

    def print_request(self, event):
        if self.print_requests:
            print({"type": event.resource_type.to_json(), "frame_id": event.frame_id, "url": event.request.url})
