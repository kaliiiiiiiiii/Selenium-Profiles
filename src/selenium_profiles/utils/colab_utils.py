import os


def restart_runtime():
    import os
    os.kill(os.getpid(), 9)


def is_collab():
    import sys
    try:
        import google.colab
        cimport = True
    except:
        cimport = False
    if ('google.colab' in sys.modules) and cimport:
        return True
    else:
        return False


def collab_installer():
    sucess = os.system('''
    apt install chromium-chromedriver >> tmp;
    apt install -y xvfb >> tmp;
    cp /usr/lib/chromium-browser/chromedriver /usr/bin >> tmp;
    zip -j /content/chromedriver_linux64.zip /usr/bin/chromedriver >> tmp;
    ''')
    with open('tmp', 'r') as f:
        out = f.read()
    patcher_src = "/usr/local/lib/python3.7/dist-packages/undetected_chromedriver/patcher.py"
    with open(patcher_src, "r") as f:
        contents = f.read()
        contents = contents.replace("return urlretrieve(u)[0]",
                                    "return urlretrieve('file:///content/chromedriver_linux64.zip',""filename='/tmp/chromedriver_linux64.zip')[0]")
    with open(patcher_src, "w") as f:
        f.write(contents)
    if sucess == 0:
        return out
    else:
        print(out)
        raise ValueError("Installation not sucessfull!!")


def update_apts():
    return os.system("apt-get update")
