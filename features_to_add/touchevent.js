
      function sendTouchEvent(x, y, element, eventType) {
            const touchObj = new Touch({
                identifier: Date.now(),
                target: element,
                clientX: x,
                clientY: y,
                pageX: x,
                pageY: y,
                radiusX: 2.5,
                radiusY: 2.5,
                rotationAngle: 10,
                force: 0.5,
            });
            const touchEvent = new TouchEvent(eventType, {
                cancelable: true,
                bubbles: true,
                touches: [touchObj],
                targetTouches: [],
                changedTouches: [touchObj],
                shiftKey: true,
            });
            element.dispatchEvent(touchEvent);
        }
        const myElement = document.getElementsByClassName('slider')[0]
        function move(ele, x, y){
            rect = ele.getBoundingClientRect()
            sendTouchEvent((rect.left + rect.right)/2, (rect.top + rect.bottom)/2, ele, 'touchstart');
            sendTouchEvent((rect.left + rect.right)/2 + x, (rect.top + rect.bottom)/2 + y, ele, 'touchmove');
            sendTouchEvent((rect.left + rect.right)/2 + x, (rect.top + rect.bottom)/2 + y,  ele, 'touchend');
        }
