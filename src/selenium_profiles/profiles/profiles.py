from collections import defaultdict

def return_profile(platform: str):
    from selenium_profiles.utils.utils import read_json
    profile = defaultdict(lambda: None)
    profile.update(read_json(filename="profiles/default.json")[platform])
    return profile  # yet supported: "Android", "Windows"


# noinspection PyPep8Naming
def Windows():
    return return_profile("Windows")


# noinspection PyPep8Naming
def Android():
    return return_profile("Android")

def example():
    from selenium_profiles.utils.utils import read_json
    example_profile = defaultdict(lambda: None )
    example_profile.update(read_json(filename="profiles/example.json"))
    return example_profile

def empty():
    profile = defaultdict(lambda: None)
    # noinspection PyTypeChecker
    profile.update({"options":{}, "cdp":{}})
    return profile
