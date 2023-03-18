from selenium_profiles.utils.utils import read, write, sel_profiles_path
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