from collections import defaultdict

class DynamicProxy:
    def __init__(self, driver, injector=None):
        self._injector = injector
        self._driver = driver
        self._seleniumwire = None

        if not self._injector:
            if "profiles" in driver.__dir__():
                if "injector" in driver.__dir__():
                    self._injector = self._driver.profiles.injector
        if "proxy" in self._driver.__dir__():
            self._seleniumwire = True
        if not(self._seleniumwire or self._injector):
            raise ModuleNotFoundError("either seleniumwire or selenium-injecter is needed for dynamic proxies")

    def str2val(self, url):
        from urllib.parse import unquote
        creds = ""
        try:
            scheme, url = url.split("://")
            if "@" in url:
                creds, url = url.split("@")
            host, port = url.split(":")
            port = int(port)
            if not (scheme and host and port):
                raise ValueError
            values = {"host": host, "port": port, "scheme": scheme}
            if creds:
                username, password = creds.split(":")
                username, password = unquote(username), unquote(password)
                if not (username and password):
                    raise ValueError
                creds = {"password": password, "username": username}
                values.update(creds)
        except ValueError:
            raise ValueError("expected proxy_url, but got " + url)
        return values

    def val2str(self, proxy_dict: dict or None, creds: dict = None):
        from urllib.parse import quote
        if proxy_dict:
            defdict = defaultdict(lambda: "")
            defdict.update(proxy_dict)
            if creds:
                # noinspection PyTypeChecker
                creds = quote(creds["username"]) + ':' + quote(creds["password"]) + '@'
            else:
                creds = ""
            parsed = defdict["scheme"] + "://" + creds + defdict["host"] + ":" + str(defdict["port"])
            return parsed

    # noinspection PyDefaultArgument
    def set_single(self, proxy, bypass_list:list or None = ["localhost", "127.0.0.1"]):
        if not bypass_list:
            bypass_list = ["localhost", "127.0.0.1"]
        if self._seleniumwire:
            self._driver.proxy = {"http":proxy, "https":proxy, "no_proxy":",".join(bypass_list)}
        elif self._injector:
            proxy = self.str2val(proxy)
            proxy.update({"bypass_list":bypass_list})
            self._injector.proxy.set_single(**proxy)

    @property
    def proxy(self):

        if self._seleniumwire:
            proxies = defaultdict(lambda: None)
            proxies.update(self._driver.proxy)
            if proxies["no_proxy"]:
                # noinspection PyUnresolvedReferences
                proxies["bypass_list"] = proxies["no_proxy"].split(",")
            del proxies["no_proxy"]
            if not proxies["http"] or proxies["https"]:
                # noinspection PyTypeChecker
                proxies["mode"] = "system"
            return dict(proxies)

        elif self._injector:
            proxy = self._injector.proxy
            mode = proxy.mode
            auth = proxy.auth
            if "urls" in auth.keys():
                del auth["urls"]
            if not auth:
                auth = None

            if mode == "fixed_servers":
                rules = defaultdict(lambda: None)
                rules.update(proxy.rules)
                bypass_list = rules["bypassList"]
                if not bypass_list:
                    bypass_list = []
                if rules["singleProxy"]:
                    # noinspection PyTypeChecker
                    single = self.val2str(rules["singleProxy"], creds=auth)
                    return {"http": single, "https": single, "ftp": single,
                            "mode": mode, "bypass_list": bypass_list,"single_proxy":True, "auth": auth}
                else:
                    return {"http": self.val2str(rules["proxyForHttp"], creds=auth),
                            "https": self.val2str(rules["proxyForHttps"], creds=auth),
                            "ftp": self.val2str(rules["proxyForFtp"], creds=auth),
                            "fallback_proxy": self.val2str(rules["fallbackProxy"], creds=auth),
                            "mode": mode, "bypass_list": bypass_list,"single_proxy":False, "auth": auth}
            else:
                return {"mode": mode, "rules": proxy.rules}
        else:
            return