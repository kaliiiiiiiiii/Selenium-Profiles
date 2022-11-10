import os
import requests
import zipfile
import shutil


def installer(dirname, url) -> (str, str):
    if os.path.isdir(os.getcwd() + "\\\\"+dirname):
        print('Updating ' + dirname + ' ...')
        shutil.rmtree(dirname)  # remove directory

    r = requests.get(url, allow_redirects=True)
    open(dirname+'.crx', 'wb').write(r.content)
    extract_del(dirname+'.crx', dirname)


def extract_del(filename, dirname) -> (str, str):
    with zipfile.ZipFile(filename, 'r') as zObject:
        zObject.extractall(path=os.getcwd() + '\\\\' + dirname)

    if os.path.isdir(os.getcwd() + "\\\\" + dirname):
        print(filename + ' extracted sucessfully!')
    else:
        raise ValueError(filename + " could not be installed correctly!")
    os.remove(filename)


def install_modheader(dirname="modheader"):
    installer(dirname,
              'https://github.com/modheader/modheader_selenium/blob/main/chrome-modheader/modheader.crx?raw=true')


def install_buster(dirname="buster"):
    installer(dirname,
              'https://github.com/dessant/buster/releases/download/v1.3.2/buster_captcha_solver_for_humans-1.3.2-chrome.zip')


if __name__ == '__main__':
    install_modheader()
    install_buster()
