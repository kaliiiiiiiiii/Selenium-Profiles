var config = {
        mode: "fixed_servers",
        rules: {
           singleProxy: {
             scheme: "%s",
             host: "%s",
             port: %s
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

globalThis.tab_event = {checked_tabs:[],tab_callback:undefined}

tab_event.req_callback = function(details) {
    var tab_id = details['tabId']
    if(tab_id >= 0){
        if(!(tab_event.checked_tabs.includes(tab_id))){
            tab_event.tab_callback(details)
            tab_event.checked_tabs.push(tab_id)
        }
    }
    else{console.log(details);}
    return {};
  }

tab_event.on_tab_removed = function(tabId) {
    var idx= tab_event.checked_tabs.indexOf(tabId);
    tab_event.checked_tabs = tab_event.checked_tabs.splice(idx, 1);
}

tab_event.set_listener = function(callback){
    tab_event.tab_callback = callback
    if(!(tab_event.tab_callback)){
        chrome.webRequest.onBeforeRequest.addListener(
          tab_event.req_callback,
          {urls: ["<all_urls>"]},
          ["blocking"]
        );
        chrome.tabs.onRemoved.addListener(tab_event.on_tab_removed)
    }
}


