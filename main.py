from spotify import MySpotify
from settings import Settings
from login import Login

from platform import system
from datetime import datetime
import traceback
import os, sys
import time


log_path = os.path.expanduser(__file__) + "/log.txt"
ads_count = Settings().get_info_from_data("ads_count")
running = True


def mute_ads():
    old_volume = mySpotify.get_volume()
    while running:
        if mySpotify.playing_advert() and mySpotify.get_volume() > 0.0:
            print(f"Muting audio. Current: {mySpotify.get_volume()}")
            old_volume = mySpotify.get_volume()
            ads_count += 1
            mySpotify.set_volume(0.0)
        elif not mySpotify.playing_advert() and mySpotify.get_volume() == 0.0:
            if old_volume is not None:
                print(f"Restoring audio to {old_volume}")
                mySpotify.set_volume(old_volume)
            else:
                print("Error getting spotify's volume.")
                sys.exit(1)

        time.sleep(1)
    on_close()


def on_close():
    Settings().set_info_in_data("ads_count", ads_count)


if __name__ == "__main__":
    try:
        # checks whether current OS is supported
        if system() not in ["Linux", "Windows"]:
            print(f"{system()} is not supported.")
            sys.exit(1)

        token = Login().return_token()
        mySpotify = MySpotify(token)

        print(f"Running on {datetime.now().date()} at {datetime.now().time()}. I have muted {ads_count} ads so far!")
        mute_ads()


    except KeyboardInterrupt:
        running = False


    except Exception as error:
        print(traceback.format_exc())

        if not os.path.exists(log_path): sys.exit(1)
        with open(log_path, "a+") as file:
            file.write(str(datetime.now()) + " - " + error.__str__() + "\n")

        on_close()