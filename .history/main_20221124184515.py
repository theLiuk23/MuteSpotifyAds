from exceptions import OsNotSupported
from login import verify_login
from spotify
from platform import system
import os, sys



### GLOBAL VARIABLES
operating_system = system() # is it running on Linux or Windows (platform library)
log_path = os.path.expanduser("~/Documents") + "/log.txt" # path where log.txt is saved
running = True # boolean that will interrupt a while loop in spotify.py


### Methods that returns local variables to other scripts
def get_operating_system() -> str:
    return operating_system

def get_log_path() -> str:
    return log_path

def is_running() -> bool:
    return running


def verify_operating_system():
    if operating_system not in ["Linux", "Windows"]:
        raise OsNotSupported(f"{operating_system} is not supported.")


### Starting point
def start():
    # checks if current running OS is supported
    verify_operating_system()
    # gets a valid token
    verify_login()
    # starts spotify.py script
    Spotify().main()



# It makes sure the script does not run when imported
if __name__ == "__main__":
    start()