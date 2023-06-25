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

patcher.toStringProxy = new Proxy(Function.prototype.toString, {
	apply: function (target, thisArg, args) {
		if (patcher.proxies.has(thisArg)) {
			return 'function '+thisArg.name+'() { [native code] }';
		}
		return target.call(thisArg);
	}
});

patcher.patch_window = function(){
    patcher.window_keys.forEach(function(key, value){
            /*var old = window[key];
            var proxy = new Proxy(window[key], {
                                   apply: function (target, thisArg, args){
                                               if(patcher.async)
                                            return undefined //target.call(thisArg, ...args);
                                        }
                                });*/
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
    //patcher.patch_window()
}

patcher.patch(false)