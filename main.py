import threading
from spotipy import Spotify, SpotifyException
from configparser import RawConfigParser
from datetime import datetime
from requests import post
from platform import system
import asyncio
import os, sys


# class containing most useful methods to control spotify's audio
class MySpotify:
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
            # if pulseaudio has an audio instance called Spotify this line will save a list containing the spotify's volumes
            volume = [self.pulse.volume_get_all_chans(key) for key in self.pulse.sink_input_list() if key.name == "Spotify"]
            if not len(volume): return 1.0 # spotify desktop isn't opened
            return round(volume[0], 2) # rounds float number by 2 digits after comma
        

    def set_volume(self, volume:float):
        if self.operating_system == "Linux":
            for key in self.pulse.sink_input_list():
                if key.name == "Spotify": self.pulse.volume_set_all_chans(key, volume)


    def playing_advert(self) -> bool:
        self.track = self.spotify.current_user_playing_track()
        if self.track is None:
            return False
        return self.track["currently_playing_type"] == "ad"


    async def main(self):
        print("hey")
        while running:
            await asyncio.sleep(1)
            if self.playing_advert():
                self.old_volume = self.get_volume()
                print(f"Muting audio: {self.old_volume}")
                self.set_volume(0.0)
            elif self.get_volume() == 0.0:
                print(f"Restoring audio: {self.old_volume}")
                self.set_volume(self.old_volume)



class Login:
    def __init__(self, base_64:str, refresh_token:str, old_token:str):
        self.time_format = r"%Y-%m-%d %H:%M:%S.%f"
        self.base_64 = base_64
        self.refresh_token = refresh_token
        self.old_token = old_token
    
        
    # it checks if the old token has expired (older than 1h)
    # if it is, a new token will be generated
    async def verify_login(self) -> str:
        last_time = Settings().get_info(data_path, "data", "last_time_token_refreshed")
        t0 = datetime.strptime(last_time, self.time_format)
        t1 = datetime.now()
        print(t0, t1, (t1-t0).total_seconds())
        if (t1 - t0).total_seconds() >= 3600:
            return await self.refresh()
        return self.old_token


    async def refresh(self) -> str:
        '''gets brand new token ready to use'''
        response = post(url = "https://accounts.spotify.com/api/token",
                        data = {"grant_type":"refresh_token",
                                "refresh_token": self.refresh_token},
                        headers = {"Authorization": "Basic " + self.base_64})

        # if access_token is in the response, the new token will be returned
        if "access_token" in response.json():
            print("Token refreshed")
            task = asyncio.create_task(self.hour_timer())
            Settings().set_info(data_path, "data", "last_time_token_refreshed", datetime.now())
            return response.json()["access_token"]
        
        # error
        print(response.json(), response.reason, response.status_code)
        sys.exit(1)

    
    async def hour_timer(self):
        await asyncio.sleep(3600)
        token = await self.refresh()
        await MySpotify(token, operating_system).main()



class Settings:
    def __init__(self):
        self.secrets_config = RawConfigParser()
        self.data_config = RawConfigParser()


    # gets a value from secrets.ini or data.ini
    def get_info(self, path:str, section:str, info:str) -> str:
        if path == data_path:
            self.data_config.read(path)
            return self.data_config.get(section, info).strip('"')
        elif path == secrets_path:
            self.secrets_config.read(path)
            return self.secrets_config.get(section, info).strip('"')


    # sets a value in secrets.ini or data.ini
    def set_info(self, path:str, section:str, info:str, value):
        with open(path, "w") as file:
            if path == data_path:
                self.data_config.read(path)
                self.data_config.set(section, info, str(value))
                self.data_config.write(file)
            elif path == secrets_path:
                self.secrets_config.read(path)
                self.secrets_config.set(section, info, str(value))
                self.secrets_config.write(file)



### GLOBAL VARIABLES
loop = asyncio.new_event_loop()
operating_system = system() # is it running on Linux or Windows (platform library)
log_path = os.path.expanduser("~/Documents") + "/log.txt" # path where log.txt is saved
secrets_path = os.path.dirname(__file__) + "/secrets.ini"
data_path = os.path.dirname(__file__) + "/data.ini"
count_ads = 0 # total muted ads in a session
running = True # boolean that will interrupt a while loop in spotify.py


# it checks if user's os is supported
def verify_operating_system():
    if operating_system not in ["Linux", "Windows"]:
        print(f"{operating_system} is not supported.")
        sys.exit(1)


### Starting point
async def start():
    # checks if current running OS is supported
    verify_operating_system()
    # gets a valid token
    base_64 = Settings().get_info(secrets_path, "secrets", "base_64")
    refresh_token = Settings().get_info(secrets_path, "secrets", "refresh_token")
    old_token = Settings().get_info(secrets_path, "secrets", "old_token")
    token = await Login(base_64, refresh_token, old_token).verify_login()
    # starts spotify.py script
    await MySpotify(token, operating_system).main()


# It makes sure the script does not run when imported
if __name__ == "__main__":
    try:
        loop.run_until_complete(start())
    except asyncio.exceptions.TimeoutError:
        loop.stop()
    except Exception as error:
        loop.stop()
        print(error.__str__())
        if not os.path.exists(log_path): sys.exit(1)
        with open(log_path, "a") as file:
            file.write(str(datetime.now()) + " - " + error.__str__() + "\n")
    finally:
        loop.stop()