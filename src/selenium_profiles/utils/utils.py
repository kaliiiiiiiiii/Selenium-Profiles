import json
import warnings
import os
import selenium_profiles


def sel_profiles_path():
    return os.path.dirname(selenium_profiles.__file__) + "/"


def write(lst: any, filename: str = 'out', encoding: str = "utf-8"):  # write list to textfile line by line
    if type(lst) is dict:
        filename = filename + '.json'
    else:
        filename = filename + '.txt'
    with open(sel_profiles_path() + filename, 'w', encoding=encoding) as fp:
        if type(lst) is list:
            fp.write(str('\n'.join(map(str, lst))))
        elif type(lst) is dict:
            fp.write(json.dumps(lst))
        elif type(lst) is str:
            fp.write(lst)
        else:
            warnings.warn("object not recognised!")
            fp.write(str(lst))
        # fp.write(str(words))
    print('Wrote to "' + filename + '"')


def read(filename: str, encoding: str = "utf-8"):
    with open(sel_profiles_path() + filename, encoding=encoding) as f:
        return f.readlines()


def read_json(filename: str = 'example.json', encoding: str = "utf-8"):
    with open(sel_profiles_path() + filename, 'r', encoding=encoding) as f:
        return json.load(f)


def write_json(obj: dict or list, filename: str = "out.json", encoding: str = "utf-8"):
    with open(sel_profiles_path() + filename, "w", encoding=encoding) as outfile:
        outfile.write(json.dumps(obj))


def find_chrome_executable():  # needed until https://github.com/ultrafunkamsterdam/undetected-chromedriver/pull/920 gets patched
    import sys
    """
    Finds the chrome, chrome beta, chrome canary, chromium executable
    Returns
    -------
    executable_path :  str
        the full file path to found executable
    """
    candidates = set()
    IS_POSIX = sys.platform.startswith(
        ("darwin", "cygwin", "linux"))  # imported from .patcher in undetected_chromedriver
    if IS_POSIX:
        for item in os.environ.get("PATH").split(os.pathsep):
            for subitem in (
                    "google-chrome",
                    "chromium",
                    "chromium-browser",
                    "chrome",
                    "google-chrome-stable",
            ):
                candidates.add(os.sep.join((item, subitem)))
        if "darwin" in sys.platform:
            candidates.update(
                [
                    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                    "/Applications/Chromium.app/Contents/MacOS/Chromium",
                ]
            )
    else:
        for item in map(
                os.environ.get, ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA", "ProgramW6432")
        ):
            if item is not None:
                for subitem in (
                        "Google/Chrome/Application",
                        "Google/Chrome Beta/Application",
                        "Google/Chrome Canary/Application",
                ):
                    candidates.add(os.sep.join((item, subitem, "chrome.exe")))
    for candidate in candidates:
        if os.path.exists(candidate) and os.access(candidate, os.X_OK):
            return os.path.normpath(candidate)
