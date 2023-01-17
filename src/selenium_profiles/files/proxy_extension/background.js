var config = {
        mode: "fixed_servers",
        rules: {
           singleProxy: {
             scheme: "%s",
             host: "%s",
             port: parseInt(%s)
           },
          bypassList: ["localhost"]
        }
    };
chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
              password: "%s"
        }
    };
}
chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
