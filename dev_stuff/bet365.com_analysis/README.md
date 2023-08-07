# bet365.com analysis

### `ProductCommon_v1.js`
- at [365365824.com/members/services/host/Scripts/js/ProductCommon_v1.js](https://www.365365824.com/members/services/host/Scripts/js/ProductCommon_v1.js)

#### `Object.toString()` patch
```js
function() {
    var f = c.lastIndexOf(this);
        if (f >= 0) {
           return d[f]
        }
        return b(this)
}
```
where C is a list of functions to patch:
```json
[
  "function toString() { [native code] }", 
  "function CustomEvent() { [native code] }", 
  "function get cancelBubble() { [native code] }", 
  "function set cancelBubble() { [native code] }", 
  "function fetch() { [native code] }", 
  "function submit() { [native code] }", 
  "function preventDefault() { [native code] }", 
  "function stopImmediatePropagation() { [native code] }", 
  "function stopPropagation() { [native code] }", 
  "function open() { [native code] }", 
  "function send() { [native code] }"
]
```

### `ProductCommon_v1.js?seed=****************` de-obfuscated
-  look like obfuscated with [Jscrambler](https://en.wikipedia.org/wiki/Jscrambler)

### `unknown.js`
- no idea where it came from (`VM171`)