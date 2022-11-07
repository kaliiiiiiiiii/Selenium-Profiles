import threading  # for exec_timeout
import time
import ctypes  # for terminate_thread
import warnings


def terminate_thread(thread):
    """Terminates a python thread from another thread.

            :param thread: a threading.Thread instance
            """
    if not thread.is_alive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def exec_timeout(target, args=None, timeout=5):
    if args is not None:
        thread = threading.Thread(target=target, args=args)  # args = (arg1,arg2,) | comma in end important!
    else:
        thread = threading.Thread(target=target)
    thread.start()
    print('going on')
    time.sleep(timeout)
    if thread.is_alive():
        terminate_thread(thread)
        timeout = str(timeout)
        warnings.warn('thread timeout! [' + timeout + ']')
    else:
        thread.join()
