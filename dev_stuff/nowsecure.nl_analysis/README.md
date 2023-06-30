# Nowsecure Cloudfare analysis
as 27.6.2023

## Service-worker scripts
overwriting javascript and emulation doesn't work there :(

#### expose emulation and `navigator.webdriver`
```js
(function() {
    var workerData = {
        p: navigator.platform,
        l: navigator.languages,
        hwC: navigator.hardwareConcurrency,
        dM: navigator.deviceMemory,
        wd: navigator.webdriver,
        uA: navigator.userAgent
    };
    postMessage(workerData);
}
)()
```

#### What's that for ??
```js
onmessage = function(e) {var gsb = function(){
    var sizeA = 0;
    var sizeB = 0;
    var counter = 0;
    try {
        var fn_1 = function () {
            counter += 1;
            fn_1();
        };
        fn_1();
    }
    catch (_a) {
        sizeA = counter;
        try {
            counter = 0;
            var fn_2 = function () {
                var local = 1;
                counter += local;
                fn_2();
            };
            fn_2();
        }
        catch (_b) {
            sizeB = counter;
        }
    }
    var bytes = (sizeB * 8) / (sizeA - sizeB);
    return [sizeA, sizeB, bytes];
}; postMessage({a3: gsb()})};
```

#### get "speed" of execution within worker
```js
function getTimingResolution() {
    var runs = 5000;
    var valA = 1;
    var valB = 1;
    var res;
    for (var i = 0; i < runs; i++) {
        var a = performance.now();
        var b = performance.now();
        if (a < b) {
            res = b - a;
            if (res > valA && res < valB) {
                valB = res;
            } else if (res < valA) {
                valB = valA;
                valA = res;
            }
        }
    }
    return valA;
};

onmessage = function(){ postMessage({ a: getTimingResolution() })}
```

#### detect open devtools  with `debugger` statement
```js
self.onmessage = function(m) {
    self.postMessage({
        o: true
    });
    eval("debugger");
    self.postMessage({
        o: false
    })
}
```

## Scripts
 look like obfuscated with [Jscrambler](https://en.wikipedia.org/wiki/Jscrambler)

### `invisible.js` de-obfuscated
- at [nowsecure.nl/cdn-cgi/challenge-platform/scripts/invisible.js](https://nowsecure.nl/cdn-cgi/challenge-platform/scripts/invisible.js)
### `v1?ray=****************.js` de-obfuscated

```js
// assumption: check function
    // args[0]: native function to check
    // args[1]: globalThis
function u(c, e) {
   e instanceof c.Function && 0 < c.Function.prototype.toString.call(e).indexOf('[native code]')
}
```
- check `.toString() == '[native code]'`
- check `instanceof Function`