from requests import post
from configparser import RawConfigParser
from spotipy import Spotify, SpotifyException
import os



def verify_login() -> str:
    last_time = get_secret_info(data_path, "data", "last_time_token_refreshed", True)



def refresh() -> str:
    '''gets brand new token ready to use'''
    response = post(url = "https://accounts.spotify.com/api/token",
                    data = {"grant_type":"refresh_token",
                                    "refresh_token": refresh_token},
                    headers = {"Authorization": "Basic " + base_64})

    print("Token refreshed")
    return response.json()["access_token"]


def get_secret_info(path:str, section:str, info:str, int_value:bool = False) -> str:
    config.read(path)
    if int_value:
        return config.getint(section, info)
    return config.get(section, info)


def set_secret_info(path:str, section:str, info:str, value):
    with open(path, "w") as file:
        config.set(section, info, str(value))
        config.write(file)



config = RawConfigParser()
secrets_path = os.path.dirname(__file__) + "/secrets.ini"
data_path = os.path.dirname(__file__) + "/data.ini"
base_64 = get_secret_info(secrets_path, "secrets", "base_64")
refresh_token = get_secret_info(secrets_path, "secrets", "refresh_token")