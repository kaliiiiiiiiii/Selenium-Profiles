import os
import requests
import zipfile
import shutil
from sel_profiles.utils.utils import sel_profiles_path


def installer(dirname, url) -> (str, str):
    if os.path.isdir(sel_profiles_path() + dirname):
        print('Updating ' + dirname + ' ...')
        shutil.rmtree(sel_profiles_path() + dirname)  # remove directory

    r = requests.get(url, allow_redirects=True)
    open(sel_profiles_path() + dirname + '.crx', 'wb').write(r.content)
    extract_del(dirname + '.crx', dirname)


def extract_del(filename, dirname) -> (str, str):
    with zipfile.ZipFile(sel_profiles_path() + filename, 'r') as zObject:
        zObject.extractall(path=sel_profiles_path() + dirname)

    if os.path.isdir(sel_profiles_path() + dirname):
        print(filename + ' extracted sucessfully!')
    else:
        raise ValueError(filename + " could not be installed correctly!")
    os.remove(sel_profiles_path() + filename)


def install_modheader(dirname=r"files\modheader"):
    installer(dirname,
              'https://github.com/modheader/modheader_selenium/blob/main/chrome-modheader/modheader.crx?raw=true')


def install_buster(dirname=r"files\buster"):
    installer(dirname,
              'https://github.com/dessant/buster/releases/download/v1.3.2/buster_captcha_solver_for_humans-1.3.2-chrome.zip')


if __name__ == '__main__':
    install_modheader()
    install_buster()
