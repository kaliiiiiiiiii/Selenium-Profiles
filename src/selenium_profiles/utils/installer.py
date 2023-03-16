from selenium_profiles.utils.utils import sel_profiles_path
from selenium_profiles.utils.colab_utils import is_colab

def my_platform():
    import platform
    if is_colab():
        return "Google-Colab"
    else:
        return platform.system()