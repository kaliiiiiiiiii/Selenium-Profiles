import os


def restart_runtime():
    import os
    os.kill(os.getpid(), 9)


def is_colab():
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
    import undetected_chromedriver
    sucess = os.system('''
    apt install chromium-chromedriver >> mytmp;
    apt install -y xvfb >> mytmp;
    cp /usr/lib/chromium-browser/chromedriver /usr/bin >> mytmp;
    zip -j /content/chromedriver_linux64.zip /usr/bin/chromedriver >> mytmp;
    ''')
    with open('mytmp', 'r') as f:
        out = f.read()
    os.remove('mytmp')
    patcher_src = os.path.dirname(undetected_chromedriver.__file__)+"/patcher.py"
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
        self.display.stop()


# noinspection PyUnresolvedReferences,PyPackageRequirements
def showscreen(driver):
    from IPython.display import display as imagerender
    from IPython.display import Image
    driver.save_screenshot('screen.png')
    imagerender(Image('screen.png'))
