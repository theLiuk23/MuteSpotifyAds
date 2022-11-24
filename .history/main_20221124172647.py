import platform
import os, sys



### GLOBAL VARIABLES
os = platform.system()
log_path = os.path.expanduser("~/Documents") + "/log.txt"
running = True


def get_os() -> str:
    return os

def get_log_path() -> str:
    return log_path

def is_running() -> bool:
    return running


def start():
    pass



if __name__ == "__main__":
    start()