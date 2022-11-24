def return_profile(platform: str):
    from selenium_profiles.utils.utils import read_json
    profile = read_json(filename="profiles\\default.json")
    return profile[platform]  # yet supported: "Android", "Windows"


# noinspection PyPep8Naming
def Windows():
    return return_profile("Windows")


# noinspection PyPep8Naming
def Android():
    return return_profile("Android")
