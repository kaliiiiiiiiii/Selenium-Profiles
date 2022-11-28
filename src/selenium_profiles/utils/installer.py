import os
import warnings
import requests
import zipfile
import shutil
import platform

from selenium_profiles.utils.utils import sel_profiles_path
from selenium_profiles.utils.colab_utils import is_collab


def my_platform():
    if is_collab:
        return "Google_Colab"
    else:
        return platform.system()


def installer(dirname, url) -> (str, str):
    if os.path.isdir(sel_profiles_path() + dirname):
        print('Updating ' + dirname + ' ...')
        shutil.rmtree(sel_profiles_path() + dirname)  # remove directory

    r = requests.get(url, allow_redirects=True)
    open(sel_profiles_path() + dirname + '.crx', 'wb').write(r.content)
    extract_del(dirname + '.crx', dirname)


def install_chromedriver(platform: str = my_platform(), chromeversion: int = 108):
    if os.path.isfile(sel_profiles_path() + "files\\chromedriver.exe"):
        print(r'Updating "files\chromedriver.exe" ..')

    # Versions
    if chromeversion == 108:
        url = 'https://chromedriver.storage.googleapis.com/108.0.5359.22/'
    elif chromeversion == 107:
        url = 'https://chromedriver.storage.googleapis.com/107.0.5304.62/'
    elif chromeversion == 106:
        url = 'https://chromedriver.storage.googleapis.com/106.0.5249.61/'
    else:
        warnings.warn("Chromedriver Version " + str(chromeversion) + " not added to installer yet!")

    # Platforms
    if platform == "Windows":
        r = requests.get(url + 'chromedriver_win32.zip')
    elif platform == "Linux":
        warnings.warn("Linux not tested yet!")
        r = requests.get(url + 'chromedriver_linux64.zip')
    else:
        warnings.warn('Chromedriver installation for "' + platform + '" not supported yet!')

    # write .zip
    open(sel_profiles_path() + r'files\chromedriver.zip', 'wb').write(r.content)
    extract_del(r'files\chromedriver.zip', dirname="files\\")


def extract_del(filename, dirname) -> (str, str):
    with zipfile.ZipFile(sel_profiles_path() + filename, 'r') as zObject:
        zObject.extractall(path=sel_profiles_path() + dirname)

    if os.path.isdir(sel_profiles_path() + dirname):
        print(filename + ' extracted to "' + dirname + '" successfully!')
    else:
        raise ValueError(
            filename + ' could not be installed correctly!, "' + dirname + '" doesn\'t exist or isn\'t a directory')
    os.remove(sel_profiles_path() + filename)


def install_modheader(dirname: str = r"files\modheader"):
    installer(dirname,
              'https://github.com/modheader/modheader_selenium/blob/main/chrome-modheader/modheader.crx?raw=true')


def install_buster(dirname: str = r"files\buster", patch_files: bool = False):
    installer(dirname,
              'https://github.com/dessant/buster/releases/download/v1.3.2/buster_captcha_solver_for_humans-1.3.2-chrome.zip')
    if patch_files:
        print('Patching "Buster" extension..')
        warnings.warn("Patch gets detected by Buster!, Not working yet.")
        patch("/files/buster/src/solve/script.js", 'mode:"closed"', 'mode:"open"')
        patch("/files/buster/src/solve/script.js.map", "mode: 'closed'", "mode: 'open'")
        patch("/files/buster/manifest.json", '"notifications",', "")
        print("\"Buster\" extension patched successfully! ")


def patch(filename: str, replace: str, replacewith: str):
    # replace string inside file
    file = open(sel_profiles_path() + filename, "rt")
    patched = file.read().replace(replace, replacewith)
    file.close()
    file = open(sel_profiles_path() + filename, "wt")
    file.write(patched)
    file.close()
    print('Patched "' + filename + '" successfully!')


if __name__ == '__main__':
    install_modheader()
    install_buster(patch_files=False)
    install_chromedriver()
