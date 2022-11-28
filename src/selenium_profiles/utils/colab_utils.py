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
