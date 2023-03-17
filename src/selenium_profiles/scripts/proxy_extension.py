from selenium_profiles.utils.utils import read, write, sel_profiles_path
def make_extension(host:str, port:int, username:str or None = None, password:str or None=None, scheme="http", temp_dir=None):
    # noinspection GrazieInspection
    """
    :param host: ip or url | str
    :param port: int
    :param username: optional
    :param password: optional
    :param scheme: "http" | "https" | "quic" | "socks4" | "socks5"

    usage:

    host = "3.144.32.194" # IP
    port = 80
    user = "user1"
    password = "my_pass"
    scheme="http"

    auth_proxy = {"host":host,"port":port,"username":user, "password":password, "scheme":scheme}

    profile["options"]["extensions"] = {"auth_proxy":auth_proxy}
    """
    schemes = ["http" , "https" , "quic" , "socks4" , "socks5"]

    if scheme in schemes:
        backgroud_js = read("files/proxy_extension/background.js") % (scheme, host, str(port), str(username), str(password))
        manifest_json = read("files/proxy_extension/manifest.json")
        write("files/tmp/proxy_extension/background.js",content=backgroud_js)
        write("files/tmp/proxy_extension/manifest.json", content=manifest_json)
        return sel_profiles_path()+"files/tmp/proxy_extension"
    else:
        raise ValueError("scheme needs to be: "+str(schemes)+",but got \""+scheme+'"')