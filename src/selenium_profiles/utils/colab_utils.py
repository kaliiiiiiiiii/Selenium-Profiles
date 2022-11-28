import os


def restart_runtime():
    import os
    os.kill(os.getpid(), 9)


def is_collab():
    import sys
    # noinspection PyBroadException
    try:
        # noinspection PyPackageRequirements
        import google.colab
        cimport = True
    except:
        cimport = False
    if ('google.colab' in sys.modules) and cimport:
        return True
    else:
        return False


def collab_installer():
    import os
    sucess = os.system('''
    apt install chromium-chromedriver >> tmp;
    apt install -y xvfb >> tmp;
    cp /usr/lib/chromium-browser/chromedriver /usr/bin >> tmp;
    zip -j /content/chromedriver_linux64.zip /usr/bin/chromedriver >> tmp;
    ''')
    with open('tmp', 'r') as f:
        out = f.read()
    os.remove('tmp')
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
        raise ValueError("Installation not successful!!")


def update_apts():
    success = os.system("apt-get update >> tmp")
    with open('tmp', 'r') as f:
        out = f.read()
    os.remove('tmp')
    if success == 0:
        return out
    else:
        print(out)
        raise ValueError("Installation not successful!!")


# noinspection PyPep8Naming
class display:
    def __init__(self):
        self.display = None

    def start_display(self, x=1200, y=2200):
        # noinspection PyUnresolvedReferences,PyPackageRequirements
        from pyvirtualdisplay import Display
        self.display = Display(visible=0, size=(x, y))
        self.display.start()

    def stop_display(self):
        self.display.stop_display()


display = display()
