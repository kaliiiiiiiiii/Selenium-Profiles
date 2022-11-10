import os
import requests
import zipfile
import shutil


def modheader_selenium(dirname):
    if os.path.isdir(os.getcwd() + "\\\\modheader"):
        print('Updating ModHeader ...')
        shutil.rmtree(dirname)  # remove directory
    url = 'https://github.com/modheader/modheader_selenium/blob/main/chrome-modheader/modheader.crx?raw=true'
    # url = 'https://github.com/requestly/modify-headers-manifest-v3/blob/master/dist/extension-1.0.0.zip?raw=true'
    r = requests.get(url, allow_redirects=True)
    open('modheader.crx', 'wb').write(r.content)
    extract_del("modheader.crx", dirname)


def extract_del(filename, dirname):
    with zipfile.ZipFile(filename, 'r') as zObject:
        zObject.extractall(path=os.getcwd() + '\\\\' + dirname)
    if os.path.isdir(os.getcwd() + "\\\\" + dirname):
        print(filename + ' extracted sucessfully!')
    else:
        raise ValueError(filename + " could not be installed correctly!")
    os.remove(filename)


if __name__ == '__main__':
    modheader_selenium("modheader")
