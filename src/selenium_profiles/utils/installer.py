import os
import warnings
import requests
import zipfile


from selenium_profiles.utils.utils import sel_profiles_path
from selenium_profiles.utils.colab_utils import is_colab


def my_platform():
    import platform
    if is_colab():
        return "Google-Colab"
    else:
        return platform.system()

def install_chromedriver(platform: str = my_platform(), chromeversion: int = 108):
    if os.path.isfile(sel_profiles_path() + "files/chromedriver.exe"):
        print(r'Updating "files/chromedriver.exe" ..')

    def write():
        # write .zip
        open(sel_profiles_path() + r'files/chromedriver.zip', 'wb').write(r.content)
        extract_del(r'files/chromedriver.zip', dirname="files/")

    # Versions
    if chromeversion == 108:
        url = 'https://chromedriver.storage.googleapis.com/108.0.5359.22/'
    elif chromeversion == 107:
        url = 'https://chromedriver.storage.googleapis.com/107.0.5304.62/'
    elif chromeversion == 106:
        url = 'https://chromedriver.storage.googleapis.com/106.0.5249.61/'
    else:
        url = None
        warnings.warn("Chromedriver Version " + str(chromeversion) + " not added to installer yet!")

    # Platforms
    if platform == "Windows":
        r = requests.get(url + 'chromedriver_win32.zip')
        write()
    elif platform == "Linux":
        warnings.warn("Linux not tested yet!")
        os.system('apt install chromium-chromedriver;apt install -y xvfb;zip -j /content/chromedriver_linux64.zip /usr/bin/chromedriver')
    elif platform == "Google-Colab":
        from selenium_profiles.utils.colab_utils import patch_uc, update_apts
        update_apts()
        os.system('apt install chromium-chromedriver;apt install -y xvfb;zip -j /content/chromedriver_linux64.zip /usr/bin/chromedriver')
        patch_uc()
    else:
        warnings.warn('Chromedriver installation for "' + platform + '" not supported yet!')


def extract_del(filename, dirname) -> (str, str):
    with zipfile.ZipFile(sel_profiles_path() + filename, 'r') as zObject:
        zObject.extractall(path=sel_profiles_path() + dirname)

    if os.path.isdir(sel_profiles_path() + dirname):
        print(filename + ' extracted to "' + dirname + '" successfully!')
    else:
        raise ValueError(
            filename + ' could not be installed correctly!, "' + dirname + '" doesn\'t exist or isn\'t a directory')
    os.remove(sel_profiles_path() + filename)


if __name__ == '__main__':
    install_chromedriver()
