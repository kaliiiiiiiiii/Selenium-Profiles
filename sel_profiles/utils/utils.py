import json
import warnings
import os


def sel_profiles_path():
    # we are in "utils", upper directory is "sel_profiles"
    if os.path.basename(os.getcwd()) == "utils" and os.path.basename(os.path.dirname(os.getcwd())) == "sel_profiles":
        return os.path.dirname(os.getcwd()) + "\\"

    # we are in "sel_profiles", "utils" is a subdirectory
    elif os.path.basename(os.getcwd()) == "sel_profiles" and "utils" in os.listdir():
        return os.getcwd() + "\\"

    # "sel_profiles" is a subdirectory, "utils" is a subdirectory of "sel_profiles"
    elif "sel_profiles" in os.listdir() and "utils" in os.listdir(os.getcwd() + "\\sel_profiles"):
        return os.getcwd() + "\\sel_profiles\\"

    # "utils" subdirectory of "sel_profiles" of "Selenium-Profiles-master"
    elif "Selenium-Profiles-master" in os.listdir() and "utils" in os.listdir(os.getcwd() + "\\Selenium-Profiles-master\\sel_profiles"):
        return os.getcwd() + "\\Selenium-Profiles-master\\sel_profiles\\"

    # where is "sel_profiles" folder?!
    else:
        raise ValueError("sel_profiles path not found!")


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
