class requests:
    def __init__(self, driver):
        self.driver = driver
        self.methods = ["GET","HEAD" "POST", "PUT", "DELETE","OPTIONS"] # TRACE, CONNECT exluded here
        self.supported_credentials = ["omit", "same-origin", "include"]
        self.modes = ["cors", "no-cors", "same-origin"]
        self.cache_values = ["default", "no-store", "reload", "no-cache", "force-cache", "only-if-cached"]
        self.redirect_values = ["follow", "error"] # "manual" excluded here
        self.referrer_policies = ["no-referrer", "no-referrer-when-downgrade", "same-origin", "origin", "strict-origin", "origin-when-cross-origin", "strict-origin-when-cross-origin", "unsafe-url"]
        self.priorities = ["high", "low", "auto"]
    def fetch(self, url: str,
              method="GET",
              headers:dict=None,
              body:str or object=None,
              mode:str=None,
              credentials:str="same-origin",
              cache:str="no-cache",
              redirect="follow",
              referrer=None,
              referer_policy = None,
              priority="high"
                    ):
        import json
        from selenium_profiles.utils.utils import read, check_cmd
        import codecs

        options = {}
        if method:
            check_cmd(method, self.methods)
            options["method"] = method
        if headers:
            options["headers"] = headers
        if body:
            if method in ["GET", "HEAD"]:
                raise ValueError("body can't be used with GET or HEAD method")
            options["body"] = body
        if mode:
            check_cmd(mode, self.modes)
            options["mode"] = mode
        if credentials:
            check_cmd(credentials, self.supported_credentials)
            options["credentials"] = credentials
        if cache:
            check_cmd(cache, self.cache_values)
            options["cache"] = cache
        if redirect:
            check_cmd(redirect, self.redirect_values)
            options["redirect"] = redirect
        if referrer:
            options["referrer"] = referrer
        if referer_policy:
            check_cmd(referer_policy,self.referrer_policies)
            options['referrerPolicy'] = referer_policy
        if priority:
            options["priority"] = priority



        options = json.dumps(options)
        url = json.dumps(url)
        js = read("js/fetch.js", sel_root=True) % (url, options)
        response = self.driver.execute_async_script(js)
        if response["status"] == "200":
            response = response["value"]
            response["content"] = codecs.decode(response["HEX"], "hex", errors="replace")
            response["text"] = response["content"].decode("utf-8", errors="replace")
            del response["HEX"]
        elif response["status"] == "error":
            raise Exception(response["stack"])

        # https://developer.mozilla.org/en-US/docs/Web/API/fetch#syntax
        return response


class actions(object):
    def __init__(self, driver):
        self.driver = driver
    def sendkeys(self, keys):  # send keys without specific Element
        from selenium.webdriver.common.action_chains import ActionChains
        action = ActionChains(self.driver)
        action.send_keys(str(keys))
        action.perform()

    def mid_location(self, element):
        return {'x': element.location_once_scrolled_into_view['x'] + (element.rect["width"] / 2),
                'y': element.location_once_scrolled_into_view['y'] + (element.rect["height"] / 2)}

# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# MODIFIED by Aurin Aegerter for Touch-actions instead of Mouse-actions

"""The TouchActionChains implementation,"""

class TouchActionChain:

    def __init__(self, driver, duration=250):
        from selenium.webdriver.common.actions.action_builder import ActionBuilder
        from selenium.webdriver.common.actions import interaction
        from selenium.webdriver.common.actions.pointer_input import PointerInput
        """Creates a new ActionChains.

        :Args:
         - driver: The WebDriver instance which performs user actions.
         - duration: override the default 250 msecs of DEFAULT_MOVE_DURATION in PointerInput
        """
        self._driver = driver
        self.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"),
                                         duration=duration)

    def perform(self):
        """Performs all stored actions."""
        self.w3c_actions.perform()

    def reset_actions(self):
        """Clears actions that are already stored locally and on the remote
        end."""
        self.w3c_actions.clear_actions()
        for device in self.w3c_actions.devices:
            device.clear_actions()

    def tap(self, on_element=None):
        """Taps an element.

        :Args:
         - on_element: The element to tap on.
           If None, taps on current touch (pointer) position.
        """
        if on_element:
            self.move_to_element(on_element)

        self.w3c_actions.pointer_action.click()
        self.w3c_actions.key_action.pause()
        self.w3c_actions.key_action.pause()

        return self

    def touch_and_hold(self, on_element=None):
        """Touch down on an element.

        :Args:
         - on_element: The element to touch down.
           If None, touches and holds on current touch (pointer) position.
        """
        if on_element:
            self.move_to_element(on_element)

        self.w3c_actions.pointer_action.click_and_hold()
        self.w3c_actions.key_action.pause()

        return self

    def context_tap(self, on_element=None):
        """Performs a context-tap (right click) on an element.

        :Args:
         - on_element: The element to context-click.
           If None, taps on current touch (pointer) position.
        """
        if on_element:
            self.move_to_element(on_element)

        self.w3c_actions.pointer_action.context_click()
        self.w3c_actions.key_action.pause()
        self.w3c_actions.key_action.pause()

        return self

    def double_tap(self, on_element=None):
        """Double-taps an element.

        :Args:
         - on_element: The element to double-tap.
           If None, taps on current touch (pointer) position.
        """
        if on_element:
            self.move_to_element(on_element)

        self.w3c_actions.pointer_action.double_click()
        for _ in range(4):
            self.w3c_actions.key_action.pause()

        return self

    def drag_and_drop(self, source, target):
        """Touches down on the source element, then moves
        to the target element and releases.

        :Args:
         - source: The element to touch down.
         - target: The element to touch up.
        """
        self.touch_and_hold(source)
        self.release(target)
        return self

    def drag_and_drop_by_offset(self, source, xoffset, yoffset):
        """Touches down on the source element, then moves
        to the target offset and releases.

        :Args:
         - source: The element to touch down.
         - xoffset: X offset to move to.
         - yoffset: Y offset to move to.
        """
        self.touch_and_hold(source)
        self.move_by_offset(xoffset, yoffset)
        self.release()
        return self

    def move_by_offset(self, xoffset, yoffset):
        """Moving the touch (pointer) to an offset from current touch (pointer).

        :Args:
         - xoffset: X offset to move to, as a positive or negative integer.
         - yoffset: Y offset to move to, as a positive or negative integer.
        """

        self.w3c_actions.pointer_action.move_by(xoffset, yoffset)
        self.w3c_actions.key_action.pause()

        return self

    def move_to_element(self, to_element):
        """Moving touch (pointer) to the middle of an element.

        :Args:
         - to_element: The WebElement to move to.
        """

        self.w3c_actions.pointer_action.move_to(to_element)
        self.w3c_actions.key_action.pause()

        return self

    def move_to_element_with_offset(self, to_element, xoffset, yoffset):
        """Move touch (pointer) by an offset of the specified element. Offsets are
        relative to the in-view center point of the element.

        :Args:
         - to_element: The WebElement to move to.
         - xoffset: X offset to move to, as a positive or negative integer.
         - yoffset: Y offset to move to, as a positive or negative integer.
        """

        self.w3c_actions.pointer_action.move_to(to_element, int(xoffset), int(yoffset))
        self.w3c_actions.key_action.pause()

        return self

    def pause(self, seconds):
        """Pause all inputs for the specified duration in seconds."""

        self.w3c_actions.pointer_action.pause(seconds)
        self.w3c_actions.key_action.pause(seconds)

        return self

    def release(self, on_element=None):
        """Releasing touch (pointer) on an element.

        :Args:
         - on_element: The element to touch up.
           If None, releases on current touch (pointer) position.
        """
        if on_element:
            self.move_to_element(on_element)

        self.w3c_actions.pointer_action.release()
        self.w3c_actions.key_action.pause()

        return self

    # Context manager so ActionChains can be used in a 'with ... as' statements.

    def __enter__(self):
        return self  # Return created instance of self.

    def __exit__(self, _type, _value, _traceback):
        pass  # Do nothing, does not require additional cleanup.
