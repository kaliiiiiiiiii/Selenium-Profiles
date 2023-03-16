import warnings


def restart_runtime():
    warnings.warn('Restarting runtime..')
    if is_colab():
        import os
        os.kill(os.getpid(), 9)
    else:
        raise EnvironmentError('Restarting environment necessary..!')


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


def show_html(driver):
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from IPython.display import display, HTML, IFrame
    display(HTML(str(driver.page_source)))


def exec_js(js: str):
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from IPython.display import Javascript
    Javascript(js)
