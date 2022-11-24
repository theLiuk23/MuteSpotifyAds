import platform
import os, sys



### GLOBAL VARIABLES
os = platform.system() # is it running on Linux or Windows
log_path = os.path.expanduser("~/Documents") + "/log.txt" # path where log.txt is saved
running = True # boolean that will interrupt a while loop in spotify.py


### Methods that returns local variables to other scripts
def get_os() -> str:
    return os

def get_log_path() -> str:
    return log_path

def is_running() -> bool:
    return running


# starting point
def start():
    pass



if __name__ == "__main__":
    start()