from login import verify_login
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
    if operating_system in ["Linux", "Windows"]:
        


### Starting point
def start():
    verify_operating_system()
    # gets a valid token
    verify_login()



# It makes sure the script does not run when imported
if __name__ == "__main__":
    start()