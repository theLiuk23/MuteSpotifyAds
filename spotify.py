from spotipy import Spotify
from platform import system


class MySpotify():
    def __init__(self, token:str):
        if system() == "Linux":
            import pulsectl
            self.pulse = pulsectl.Pulse()
        self.spotify = Spotify(auth=token)


    def get_volume(self) -> float:
        if system() == "Linux":
            # if pulseaudio has an audio instance called Spotify this line will save a list containing the spotify's volumes
            for key in self.pulse.sink_input_list():
                if key.name == "Spotify":
                    return round(self.pulse.volume_get_all_chans(key), 2)
            return 0.0


    def set_volume(self, volume:float):
        if system() == "Linux":
            for key in self.pulse.sink_input_list():
                if key.name == "Spotify":
                    self.pulse.volume_set_all_chans(key, volume)


    def playing_advert(self) -> bool:
        track = self.spotify.current_user_playing_track()
        if track is None:
            return False
        return track["currently_playing_type"] == "ad"