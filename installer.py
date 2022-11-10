import os
import requests
import zipfile


def modheader_selenium():
    if os.path.isdir(os.getcwd() + "\\\\modheader"):
        print('Updating ModHeader ...')
    url = 'https://github.com/modheader/modheader_selenium/blob/main/chrome-modheader/modheader.crx?raw=true'
    r = requests.get(url, allow_redirects=True)
    open('modheader.crx', 'wb').write(r.content)
    extract_del("modheader.crx", "modheader")


def extract_del(filename, dirname):
    with zipfile.ZipFile(filename, 'r') as zObject:
        zObject.extractall(path=os.getcwd() + '\\\\' + dirname)
    if os.path.isdir(os.getcwd() + "\\\\" + dirname):
        print(filename + ' extracted sucessfully!')
    else:
        raise ValueError(filename + " could not be installed correctly!")
    os.remove(filename)


if __name__ == '__main__':
    modheader_selenium()
