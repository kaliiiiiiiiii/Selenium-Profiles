(function () {
  'use strict';

  function captureEvents(events) {
    const captured = events.map(captureEvent);

    return () => captured.forEach((t) => t())

    function captureEvent(event) {
      let isCapturePhase = true;

      // eslint-disable-next-line @typescript-eslint/ban-types
      const callbacks = new Map();
      const eventArgs = new Set();

      // This is the only listener for the native event
      event.addListener(handleEvent);

      function handleEvent(...args) {
        if (isCapturePhase) {
          // This is before dynamic import completes
          eventArgs.add(args);

          if (typeof args[2] === 'function') {
            // During capture phase all messages are async
            return true
          } else {
            // Sync messages or some other event
            return false
          }
        } else {
          // The callbacks determine the listener return value
          return callListeners(...args)
        }
      }

      // Called when dynamic import is complete
      //  and when subsequent events fire
      function callListeners(...args) {
        let isAsyncCallback = false;
        callbacks.forEach((options, cb) => {
          // A callback error should not affect the other callbacks
          try {
            isAsyncCallback = cb(...args) || isAsyncCallback;
          } catch (error) {
            console.error(error);
          }
        });

        if (!isAsyncCallback && typeof args[2] === 'function') {
          // We made this an async message callback during capture phase
          //   when the function handleEvent returned true
          //   so we are responsible to call sendResponse
          // If the callbacks are sync message callbacks
          //   the sendMessage callback on the other side
          //   resolves with no arguments (this is the same behavior)
          args[2]();
        }

        // Support events after import is complete
        return isAsyncCallback
      }

      // This function will trigger this Event with our stored args
      function triggerEvents() {
        // Fire each event for this Event
        eventArgs.forEach((args) => {
          callListeners(...args);
        });

        // Dynamic import is complete
        isCapturePhase = false;
        // Don't need these anymore
        eventArgs.clear();
      }

      // All future listeners are handled by our code
      event.addListener = function addListener(cb, ...options) {
        callbacks.set(cb, options);
      };

      event.hasListeners = function hasListeners() {
        return callbacks.size > 0
      };

      event.hasListener = function hasListener(cb) {
        return callbacks.has(cb)
      };

      event.removeListener = function removeListener(cb) {
        callbacks.delete(cb);
      };

      event.__isCapturedEvent = true;

      return triggerEvents
    }
  }

  function delay(ms) {
    return new Promise((resolve) => {
      setTimeout(resolve, ms);
    })
  }

  /**
   * Get matches from an object of nested objects
   *
   * @export
   * @template T Type of matches
   * @param {*} object Parent object to search
   * @param {(x: any) => boolean} pred A predicate function that will receive each property value of an object
   * @param {string[]} excludeKeys Exclude a property if the key exactly matches
   * @returns {T[]} The matched values from the parent object
   */
  function getDeepMatches(object, pred, excludeKeys) {
    const keys = typeof object === 'object' && object ? Object.keys(object) : [];

    return keys.length
      ? keys
          .filter((key) => !excludeKeys.includes(key))
          .reduce((r, key) => {
            const target = object[key];

            if (target && pred(target)) {
              return [...r, target]
            } else {
              return [...r, ...getDeepMatches(target, pred, excludeKeys)]
            }
          }, [] )
      : []
  }

  const importPath = /*@__PURE__*/ JSON.parse('"../js/background.js"'); 
  const delayLength = /*@__PURE__*/ JSON.parse('0'); 
  const excludedPaths = /*@__PURE__*/ JSON.parse('["extension"]');

  const events = getDeepMatches(
    chrome,
    (x) => typeof x === 'object' && 'addListener' in x,
    // The webRequest API is not compatible with event pages
    //  TODO: this can be removed
    //   if we stop using this wrapper with "webRequest" permission
    excludedPaths.concat(['webRequest']),
  );
  const triggerEvents = captureEvents(events);

  import(importPath).then(async () => {
    if (delayLength) await delay(delayLength);

    triggerEvents();
  });

})();
