from login import verify_login
from platform import system
import os, sys


### GLOBAL VARIABLES
operating_system = system() # is it running on Linux or Windows (platform library)
log_path = os.path.expanduser("~/Documents") + "/log.txt" # path where log.txt is saved
count_ads = 0 # total muted ads in a session
running = True # boolean that will interrupt a while loop in spotify.py


### Methods that get or set local variables to other scripts
# def operating_system(value:str=None) -> str:
#     if value is None:
#         return operating_system
#     operating_system = value

# def log_path(value:str=None) -> str:
#     if value is None:
#         return log_path
#     log_path = value

# def count_ads(value:int=None) -> int:
#     if value is None:
#         return count_ads
#     count_ads = value

# def running(value:bool=None) -> bool:
#     if value is None:
#         return running
#     running = value


def verify_operating_system() -> bool:
    if operating_system not in ["Linux", "Windows"]:
        print(f"{operating_system} is not supported.")
        return False
    return True


### Starting point
def start():
    # checks if current running OS is supported
    if not verify_operating_system():
        sys.exit(1)
    # gets a valid token
    token = verify_login()
    # starts spotify.py script
    from my_spotify import MySpotify
    MySpotify(token, operating_system).main()



# It makes sure the script does not run when imported
if __name__ == "__main__":
    start()