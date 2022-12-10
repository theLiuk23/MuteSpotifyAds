from spotify import MySpotify
from settings import Settings
from login import Login

from platform import system
from datetime import datetime
from PIL import Image
import traceback
import pystray
import os, sys
import time


# icon closing
def on_close(icon, item):
    print("Closing...")
    icon.stop()
    sys.exit(0)


log_path = os.path.dirname(__file__) + "/log.txt"
running = True

icon = pystray.Icon(
    name='Spotify is playing some music',
    icon=Image.open(os.path.dirname(__file__) + "/volume.png"),
    menu=pystray.Menu(pystray.MenuItem("Close", on_close))
)


def add_ads_count():
    # adds 1 to the ad count in data.ini
    old_value = int(Settings().get_info_from_data("ads_count"))
    Settings().set_info_in_data("ads_count", old_value + 1)


def mute_ads(icon):
    icon.visible = True
    old_volume = mySpotify.get_volume()

    while running:
        # if token is not valid anymore it will be updated in spotify.py scipt
        if not Login().verify_login():
            mySpotify.update_token(Login().return_token())

        if mySpotify.playing_advert() and mySpotify.get_volume() > 0.0:
            print(f"Muting audio. Current: {old_volume}")
            old_volume = mySpotify.get_volume()
            mySpotify.set_volume(0.0)
            add_ads_count() # adds 1 to the ad count in data.ini
        elif not mySpotify.playing_advert() and mySpotify.get_volume() == 0.0:
            if old_volume is not None:
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

        print(f"Running on {datetime.now().date()} at {datetime.now().time()}")
        icon.run(mute_ads)

    except KeyboardInterrupt:
        ads_count = Settings().get_info_from_data("ads_count")
        print(f"I have muted {ads_count} ads so far")

    except TimeoutError:
        token = Login().return_token()
        mySpotify.update_token(token)
        print(f"Running on {datetime.now().date()} at {datetime.now().time()}")
        icon.stop()
        icon.run(mute_ads)

    except Exception as error:
        print(traceback.format_exc())
        if not os.path.exists(log_path): sys.exit(1)
        with open(log_path, "a+") as file:
            file.write(str(datetime.now()) + " - " + error.__str__() + "\n")