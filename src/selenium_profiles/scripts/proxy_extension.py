from selenium_profiles.utils.utils import read, write, sel_profiles_path

def make_extension(host:str, port:int, username:str, password:str):
    backgroud_js = read("files/proxy_extension/background.js") % (host, str(port), username, password)
    manifest_json = read("files/proxy_extension/manifest.json")
    write("files/tmp/proxy_extension/background.js",content=backgroud_js)
    write("files/tmp/proxy_extension/manifest.json", content=manifest_json)
    return sel_profiles_path()+"files/tmp/proxy_extension"