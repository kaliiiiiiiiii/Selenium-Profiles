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
    import ast
    import subprocess
    out = subprocess.run(['apt install chromium-chromedriver;apt install -y xvfb;cp /usr/lib/chromium-browser/chromedriver /usr/bin;zip -j /content/chromedriver_linux64.zip /usr/bin/chromedriver'], stdout=subprocess.PIPE)
    patcher_src = "/usr/local/lib/python3.7/dist-packages/undetected_chromedriver/patcher.py"
    with open(patcher_src, "r") as f:
        contents = f.read()
        contents = contents.replace("return urlretrieve(u)[0]",
                                    "return urlretrieve('file:///content/chromedriver_linux64.zip',""filename='/tmp/chromedriver_linux64.zip')[0]")
    with open(patcher_src, "w") as f:
        f.write(contents)

    return ast.literal_eval(str(out.stdout))


def update_apts():
    return os.system("apt-get update")
