import json
import warnings
import os
import selenium_profiles


def sel_profiles_path():
    return os.path.dirname(selenium_profiles.__file__) + "/"


def read(filename: str, encoding: str = "utf-8"):
    with open(sel_profiles_path() + filename, encoding=encoding) as f:
        return f.read()

def write(filename: str, content:str, encoding: str = "utf-8"):
    with open(sel_profiles_path() + filename,"w", encoding=encoding) as f:
        return f.write(content)

def read_json(filename: str = 'example.json', encoding: str = "utf-8"):
    with open(sel_profiles_path() + filename, 'r', encoding=encoding) as f:
        return json.load(f)


def write_json(obj: dict or list, filename: str = "out.json", encoding: str = "utf-8"):
    with open(sel_profiles_path() + filename, "w", encoding=encoding) as outfile:
        outfile.write(json.dumps(obj))
