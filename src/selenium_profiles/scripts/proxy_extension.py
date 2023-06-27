from selenium_profiles.utils.utils import read, write, sel_profiles_path
from collections import defaultdict

from selenium_profiles.webdriver import profiles


def make_extension(host:str, port:int, username:str or None = None, password:str or None=None, scheme:str="http", temp_dir:str=None):
    # noinspection GrazieInspection
    """
    :param host: ip or url | str
    :param port: int
    :param username: str, optional
    :param password: optional
    :param scheme: "http" | "https" | "quic" | "socks4" | "socks5"
    :param temp_dir: str, optional

    usage:

    host = "3.144.32.194" # IP
    port = 80
    user = "user1"
    password = "my_pass"
    scheme="http"

    auth_proxy = {"host":host,"port":port,"username":user, "password":password, "scheme":scheme, "temp_dir": "C:/Downloads/proxy_extension"}

    profile["options"]["extensions"] = {"auth_proxy":auth_proxy}
    """
    schemes = ["http" , "https" , "quic" , "socks4" , "socks5"]
    if temp_dir is None:
        temp_dir = sel_profiles_path()+"files/tmp/proxy_extension/"
    else:
        if temp_dir[-1] != "/" or temp_dir[-1] != "\\":
            temp_dir += "/"
    if scheme in schemes:
        background_js = read("files/proxy_extension/background.js", sel_root=True) % (scheme, host, str(port), str(username), str(password))
        manifest_json = read("files/proxy_extension/manifest.json", sel_root=True)
        write(temp_dir+"background.js",content=background_js, sel_root=False)
        write(temp_dir+"manifest.json", content=manifest_json, sel_root=False)
        return temp_dir[:-1] # remove "/" in the end
    else:
        raise ValueError("scheme needs to be: "+str(schemes)+",but got \""+scheme+'"')

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
        creds = ""
        try:
            scheme, url = url.split("://")
            if "@" in url:
                creds, url = url.split("@")
            host, port = url.split(":")
            values = {"host": host, "port": port, "scheme": scheme}
            if creds:
                username, password = creds.split(":")
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
    def set_single(self, proxy, bypass_list:list = ["localhost", "127.0.0.1"]):
        if self._seleniumwire:
            self._driver.proxy = {"http":proxy, "https":proxy, "no_proxy":",".join(bypass_list)}
        elif self._injector:
            raise NotImplementedError("dynamic proxies with injector not implemented yet")
            #self._injector.proxy.set_single()

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