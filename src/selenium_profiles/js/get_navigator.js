function roundHalf(num) { // round to half int
    if (typeof num === 'number') {return Math.round(num*2)/2}
    else {return null}
};

function copyToClipboard(text){
        window.prompt("Copy to clipboard: Ctrl+C, Enter", text);
    };

function a(elem, replace=null){ // replace non_existing variables with null
    try{elem = eval(elem)}
    catch{elem = replace};
     //if_exist, else null
     if (typeof elem !== 'undefined') {return elem} else {return replace};
};

function build_navigator() {
    wow64 = a(navigator.userAgent.indexOf('WOW64')>-1);

    maxtouchpoints = a('window.navigator.maxTouchPoints');
    if (maxtouchpoints > 16 || maxtouchpoints < 1){maxtouchpoints=10}

    orient_type = a('screen.orientation.type')

    // fix orientation type Values
    if (orient_type === 'portrait-primary'){orient_type = "portraitPrimary"}
    if (orient_type === 'landscape-primary'){orient_type = "landscapePrimary"}

    my_screen = {
        "mobile":a('navigator.userAgentData.mobile'),
        "width": a('screen.width'),
        "height": a('screen.height'),
        "deviceScaleFactor": roundHalf(a('window.devicePixelRatio')),
            "screenOrientation": {
                "type": orient_type,
                "angle": a('screen.orientation.angle')}}

    my_navigator = {
        "cdp": {
            "touch": (('ontouchstart' in window) || (maxtouchpoints > 0)),
            "maxtouchpoints": maxtouchpoints,
            "emulation": my_screen,
            "cores":a("navigator.hardwareConcurrency"),
            "useragent": {
                  "platform": a('navigator.platform'),
                  "acceptLanguage":a('navigator.language') || a('navigator.userLanguage'),
                  "userAgent": a('navigator.userAgent'),
                  "userAgentMetadata": {
                       "brands": window.useragent["brands"],
                       "fullVersionList": window.useragent["fullVersionList"],
                       "fullVersion": window.useragent["uaFullVersion"],
                       "platform": window.useragent["platform"],
                       "platformVersion": window.useragent["platformVersion"],
                       "architecture": window.useragent["architecture"],
                       "model": window.useragent["model"],
                       "mobile": window.useragent["mobile"],
                       "bitness": window.useragent["bitness"],
                       "wow64": window.wow64}
                  }
            }
        }
    return my_navigator
 }

console.log('Getting Profile..')
window.useragent_set = false;
navigator.userAgentData.getHighEntropyValues( // get useragent
    ["architecture",
    "model",
    "platformVersion",
    "bitness",
    "uaFullVersion",
    "fullVersionList"])
    .then((values) => {
        window.useragent = values;
        console.log(values);
        window.useragent = build_navigator();
        window.useragent_set = true
        return window.useragent;
        //copyToClipboard(JSON.stringify(window.navigator()));
    });


