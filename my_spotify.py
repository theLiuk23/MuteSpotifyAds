from spotipy import Spotify
import pulsectl


class MySpotify:
    def __init__(self, token:str, platform:str):
        self.track:dict = None
        self.spotify = Spotify(auth=token)
        self.platform:str = platform
        self.old_volume:float = self.get_current_volume()


    def get_current_volume(self) -> float:
        if self.platform == "Linux":
            pulse = pulsectl.Pulse()
            # if pulseaudio has an audio instance called Spotify this line will save a list containing the spotify's volumes
            volume = [pulse.volume_get_all_chans(key) for key in pulse.sink_input_list() if key.name == "Spotify"]
            if not len(volume): return 0.0 # spotify desktop isn't opened
            return round(volume[0], 2) # rounds float number by 2 digits after comma


    def main(self):
        pass