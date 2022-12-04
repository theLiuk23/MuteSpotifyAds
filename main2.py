from spotify import MySpotify
from login import Login
from platform import system
from datetime import datetime
import traceback
import os, sys
import time


log_path = os.path.expanduser(__file__) + "/log.txt"
old_volume = None


def mute_ads():
    while True:
        if mySpotify.playing_advert() and mySpotify.get_volume() > 0.0:
            print(f"Muting audio. Current: {mySpotify.get_volume()}")
            old_volume = mySpotify.get_volume()
            mySpotify.set_volume(0.0)
        elif not mySpotify.playing_advert() and mySpotify.get_volume() <= 0.0:
            if old_volume:
                print(f"Restoring audio to {old_volume}")
                mySpotify.set_volume(old_volume)
            else:
                print("Error getting spotify's volume.")
                sys.exit(1)

        time.sleep(1)


if __name__ == "__main__":
    try:
        # checks whether current OS is supported
        if system() not in ["Linux", "Windows"]:
            print(f"{system()} is not supported.")
            sys.exit(1)

        token = Login().return_token()
        mySpotify = MySpotify(token)
        old_volume = mySpotify.get_volume()

        print(f"Running on {datetime.now().date()} at {datetime.now().time()}")
        mute_ads()


    except KeyboardInterrupt:
        sys.exit(0)


    except Exception as error:
        print(traceback.format_exc())
        if not os.path.exists(log_path): sys.exit(1)
        with open(log_path, "a+") as file:
            file.write(str(datetime.now()) + " - " + error.__str__() + "\n")