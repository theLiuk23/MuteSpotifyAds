from configparser import RawConfigParser
from multiprocessing import Process
from datetime import datetime
import webbrowser
from spotipy import Spotify
from platform import system
from requests import post
import traceback
import time
import os, sys
import wx, wx.adv


# class containing most useful methods to control spotify's audio
class MySpotify():
    def __init__(self, token:str, operating_system:str):
        self.track:dict = None
        self.spotify = Spotify(auth=token)
        self.operating_system:str = operating_system
        if self.operating_system == "Linux":
            import pulsectl
            self.pulse = pulsectl.Pulse()
        self.old_volume:float = self.get_volume()


    def get_volume(self) -> float:
        if self.operating_system == "Linux":
            volume = None
            # if pulseaudio has an audio instance called Spotify this line will save a list containing the spotify's volumes
            for key in self.pulse.sink_input_list():
                if key.name == "Spotify":
                    volume = self.pulse.volume_get_all_chans(key)
            if volume is None:
                return 1.0 # spotify desktop isn't opened
            return round(volume, 2) # rounds float number by 2 digits after comma


    def set_volume(self, volume:float):
        if self.operating_system == "Linux":
            for key in self.pulse.sink_input_list():
                if key.name == "Spotify":
                    self.pulse.volume_set_all_chans(key, volume)


    def playing_advert(self) -> bool:
        self.track = self.spotify.current_user_playing_track()
        if self.track is None:
            return False
        return self.track["currently_playing_type"] == "ad"


    def main(self):
        while running:
            # checks if token expires while the script is running
            if not Login().verify_login():
                start()

            # ad is being played, volume has to be muted
            if self.playing_advert() and self.get_volume() > 0.0:
                # saves volume's value before muting it
                self.old_volume = self.get_volume()
                print(f"Muting audio:    {self.old_volume}")
                IconApp().icon.set_icon(os.path.dirname(__file__) + "/mute.png")
                self.set_volume(0.0)
            # ad stopped being played, volume has to be restored
            elif not self.playing_advert() and self.get_volume() <= 0.0:
                print(f"Restoring audio: {self.old_volume}")
                self.set_volume(self.old_volume)
                IconApp().icon.set_icon(os.path.dirname(__file__) + "/volume.png")

            time.sleep(1)
        print("The end")



class Login:
    def __init__(self):
        self.time_format = r"%Y-%m-%d %H:%M:%S.%f"
        self.base_64 = Settings().get_info_from_secrets("base_64")
        self.refresh_token = Settings().get_info_from_secrets("refresh_token")
        self.old_token = Settings().get_info_from_secrets("old_token")
        self.last_time = Settings().get_info_from_data("last_time_token_refreshed")
    
        
    # it checks if the old token has expired (older than 1h)
    def verify_login(self) -> bool:
        t0 = datetime.strptime(self.last_time, self.time_format)
        t1 = datetime.now()
        # print(t0, t1, (t1-t0).total_seconds())
        if (t1 - t0).total_seconds() >= 3600:
            return False
        return True


    def return_token(self) -> str:
        if not self.verify_login():
            self.refresh()
        return self.old_token


    def refresh(self):
        '''gets brand new token ready to use'''
        response = post(url = "https://accounts.spotify.com/api/token",
                        data = {"grant_type":"refresh_token",
                                "refresh_token": self.refresh_token},
                        headers = {"Authorization": "Basic " + self.base_64})

        # if access_token is in the response, the new token will be returned
        if "access_token" in response.json():
            token = response.json()["access_token"]
            print(f"Token refreshed")
            Settings().set_info_in_data("last_time_token_refreshed", datetime.now())
            Settings().set_info_in_secrets("old_token", token)
            self.last_time = str(datetime.now())
            self.old_token = token

        else:
            print("I could not refresh the token. Exiting.")
            sys.exit(1)



class Settings:
    def __init__(self):
        self.secrets_config = RawConfigParser()
        self.data_config = RawConfigParser()
        self.secrets_config.read(secrets_path)
        self.data_config.read(data_path)


    # gets a value from secrets.ini
    def get_info_from_secrets(self, info:str) -> str:
        return self.secrets_config.get("secrets", info).strip('"')

    # gets a value from  data.ini
    def get_info_from_data(self, info:str) -> str:
        return self.data_config.get("data", info).strip('"')

    # sets a value in secrets.ini
    def set_info_in_secrets(self,info:str, value):
        with open(secrets_path, "w") as file:
            self.secrets_config.set("secrets", info, str(value))
            self.secrets_config.write(file)

    # sets a value in data.ini
    def set_info_in_data(self, info:str, value):
        with open(data_path, "w") as file:
            self.data_config.set("data", info, str(value))
            self.data_config.write(file)


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame:wx.Frame):
        self.TRAY_TOOLTIP = 'Name' 
        self.TRAY_ICON = os.path.dirname(__file__) + "/volume.png" 
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(self.TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        self.create_menu_item(menu, 'Site', self.on_hello)
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def create_menu_item(self, menu, label, func):
        item = wx.MenuItem(menu, -1, label)
        menu.Bind(wx.EVT_MENU, func, id=item.GetId())
        menu.Append(item)
        return item

    def on_left_down(self, event):
        pass

    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, self.TRAY_TOOLTIP)

    def on_hello(self, event):
        webbrowser.open('https://www.github.com/theLiuk23/MuteSpotifyAds2')

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.DeletePendingEvents()
        print("Boh")
        self.frame.Close()
        print("forse")
        raise ChildProcessError


class IconApp(wx.App):
    icon:TaskBarIcon = None

    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        icon = TaskBarIcon(frame)
        return True


class StartIcon():
    def __init__(self):
        self.iconApp = IconApp()

    def main(self):
        self.iconApp.MainLoop()

    def stop(self):
        self.iconApp.ExitMainLoop()




# It makes sure the script does not run when imported
if __name__ == "__main__":
    ### GLOBAL VARIABLES
    operating_system = system() # is it running on Linux or Windows (platform library)
    log_path = os.path.expanduser("~/Documents") + "/log.txt" # path where log.txt is saved
    secrets_path = os.path.dirname(__file__) + "/secrets.ini"
    data_path = os.path.dirname(__file__) + "/data.ini"
    count_ads = 0 # total muted ads in a session
    running = True # boolean that will interrupt a while loop in spotify.py
    process = Process(target=StartIcon().main, daemon=False)


    # it checks if user's OS is supported
    def verify_operating_system():
        if operating_system not in ["Linux", "Windows"]:
            print(f"{operating_system} is not supported.")
            sys.exit(1)


    ### Starting point
    def start():
        # checks if current running OS is supported
        verify_operating_system()
        # gets a valid token
        token = Login().return_token()
        # running icon on a new thread
        process.start()
        # running mySpotify on main thread
        MySpotify(token, operating_system).main()


    try:
        start()

    except Exception as error:
        print(traceback.format_exc())
        if not os.path.exists(log_path): sys.exit(1)
        with open(log_path, "a") as file:
            file.write(str(datetime.now()) + " - " + error.__str__() + "\n")