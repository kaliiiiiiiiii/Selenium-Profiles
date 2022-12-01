import os
import pathlib
import re
import subprocess
import typing
import warnings


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


def is_jupyter() -> bool:
    """It checks whether a module is run from a Jupyter notebook"""
    try:
        # noinspection PyUnresolvedReferences,PyStatementEffect
        get_ipython
        return True
    except NameError:
        # noinspection PyTypeChecker
        return


def get_module_path(module: str) -> typing.Optional[pathlib.Path]:
    """It gets the absolute path of a Python module"""
    r = subprocess.run(
        ["pip", "show", module],
        capture_output=True
    )

    try:
        r.check_returncode()
    except subprocess.CalledProcessError:
        return None

    stdout = r.stdout.decode()

    try:
        RE_abspath = '\nLocation: (?P<abspath>.*)\n'
        abspath = re.search(RE_abspath, stdout).group('abspath')
    except AttributeError:
        return None

    return pathlib.Path(abspath).absolute()


def patch_uc(src: str = '/content/chromedriver_linux64.zip',
             dst: str = '/tmp/chromedriver_linux64.zip') -> None:
    from selenium_profiles.utils.colab_utils import restart_runtime
    PY_uc = 'undetected_chromedriver'
    """It forces undetected_chromedriver to run the webdriver on Chromium

    It patches 'undetected_chromedriver/patcher.py' to make it work on Google Colab
    by forcing the webdriver to run on Chromium, which has less stringent constraints.

    Parameters
    ----------
    src
        The src Chromium webdriver abspath

    dst
        The dst Chromium webdriver abspath
    """
    if not is_colab():
        warnings.warn('Patching undetected-chromedriver in non-google-colab')

    dirpath = get_module_path(PY_uc)

    if dirpath is None:
        warnings.warn(
            f"Cannot find the {PY_uc} module. "
            f"If you want to use undetected-chromedriver"
            f"you can install it with 'pip install {PY_uc}'"
            f"and then run in Python:"
            f"from selenium_profiles.utils.colab_utils import patch_uc"
            f"patch_uc()"
        )
        return

    N_patcher_src = dirpath / PY_uc / 'patcher.py'
    O_patcher_src = dirpath / PY_uc / 'patcher_O.py'

    if O_patcher_src.exists():
        return

    with N_patcher_src.open('rt') as f:
        contents = f.read()

        with O_patcher_src.open('wt') as g:
            g.write(contents)

        contents = contents.replace(
            "return urlretrieve(u)[0]",
            "return urlretrieve("
            f"'file://{src}', "
            f"'{dst}'"
            ")[0]"
        )

    with N_patcher_src.open('wt') as f:
        f.write(contents)

    if is_colab():
        restart_runtime()


def update_apts():
    success = os.system("apt-get update >> mytmp")
    with open('mytmp', 'r') as f:
        out = f.read()
    os.remove('mytmp')
    if success == 0:
        return out
    else:
        print(out)
        raise ValueError("Updates not successful!!")


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
