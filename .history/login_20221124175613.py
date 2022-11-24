from requests import post
from configparser import RawConfigParser
from spotipy import Spotify, SpotifyException
import os



def verify_login() -> str:
    


def refresh() -> str:
    '''gets brand new token ready to use'''
    response = post(url = "https://accounts.spotify.com/api/token",
                    data = {"grant_type":"refresh_token",
                                    "refresh_token": refresh_token},
                    headers = {"Authorization": "Basic " + base_64})

    print("Token refreshed")
    return response.json()["access_token"]


def get_secret_info(info:str) -> str:
    config.read(secrets_path)
    return config.get("secrets", info)


def set_secret_info(info:str, value):
    with open(secrets_path, "w") as file:
        config.set("secrets", info, value)
        config.write(file)



config = RawConfigParser()
secrets_path = os.path.dirname(__file__) + "/secrets.ini"
base_64 = get_secret_info("base_64")
refresh_token = get_secret_info("refresh_token")