import os
import requests
import zipfile


def install():
    url = 'https://github.com/modheader/modheader_selenium/blob/main/chrome-modheader/modheader.crx?raw=true'
    r = requests.get(url, allow_redirects=True)
    open('modheader.crx', 'wb').write(r.content)
    with zipfile.ZipFile("modheader.crx", 'r') as zObject:
        zObject.extractall(path=os.getcwd() + '\\\\modheader')
    if os.path.isdir(os.getcwd() + "\\\\modheader"):
        print('ModHeader extracted sucessfully!')
    else:
        raise ValueError("Modheader could not be installed correctly!")
    os.remove("modheader.crx")


if __name__ == '__main__':
    install()
