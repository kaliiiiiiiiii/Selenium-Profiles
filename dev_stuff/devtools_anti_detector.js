patcher = {}
patcher.proxies = new Set()
patcher.window_keys = ['debug','dir', 'table', 'clear', 'profile', 'profileEnd']

patcher.console_keys = ["clear",'debug', 'error', 'info', 'log', 'warn', 'dir', 'dirxml', 'table', 'trace', 'group', 'groupCollapsed', 'groupEnd', 'count', 'countReset', 'assert', 'profile', 'profileEnd', 'time', 'timeLog', 'timeEnd', 'timeStamp', 'context', 'createTask']

patcher.sync2async = async function exec(func, args){func(...args)}

patcher.console_handler = {
    get(target, prop, receiver){
        if (patcher.console_keys.includes(prop)){
            var func = Reflect.get(...arguments);
            var proxied_func = new Proxy(func, {
                               apply: function (target, thisArg, args){
                                       if (patcher.async){patcher.sync2async(func, args)}
                                        return
                                    }
                            });
            patcher.proxies.add(proxied_func)
            return proxied_func
           }
        return Reflect.get(target, prop, arguments);
    }
}

// window.catch = function(...args){console.log(args), throw(...args)}

patcher.toStringProxy = new Proxy(Function.prototype.toString, {
	apply: function (target, thisArg, args) {
		if (patcher.proxies.has(thisArg)) {
			return 'function '+thisArg.name+'() { [native code] }';
		}
		try{return target.call(thisArg)}
		catch(e){e = new Proxy(e, patcher.TypeError_handler); throw e}
	}
});

patcher.TypeError_handler = {get(target, prop, receiver){
        if (prop == "stack"){
            stack = Reflect.get(target, prop, arguments).split("\n")
            stack.splice(-2, 1);
            return stack.join("\n")
           }
        return Reflect.get(target, prop, arguments);
    }
}

patcher.patch_window = function(){
    patcher.window_keys.forEach(function(key, value){
            window[key] = console[key];
            patcher.proxies.add(window[key])
        });
}


patcher.patch = function(async=false){
    patcher.patch_window()
    patcher.async = async;
    window.console = new Proxy(window.console, patcher.console_handler);
    Function.prototype.toString = patcher.toStringProxy;
    patcher.proxies.add(Function.prototype.toString);
    patcher.patch_window()
}
try{console.log.toString.call(4)}catch(e){before = e}
patcher.patch(true)
try{console.log.toString.call(4)}catch(e){after = e}