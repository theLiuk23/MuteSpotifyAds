import platform
import os, sys



### GLOBAL VARIABLES
os = platform.system()
log_path = os.path.expanduser("~/Documents") + "/log.txt"
running = True


def get_os():
    return os


def start():
    pass



if __name__ == "__main__":
    start()