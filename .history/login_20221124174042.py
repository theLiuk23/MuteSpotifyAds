from requests import post
from configparser import RawConfigParser
import os


config = RawConfigParser()
secrets_path = __file__.removesuffix(__name__) + "secrets.ini"


def verify_login() -> str:
    pass



def refresh(self) -> str:
    '''gets brand new token ready to use'''
    response = post(url = "https://accounts.spotify.com/api/token",
                            data = {"grant_type":"refresh_token",
                                    "refresh_token": self.refresh_token},
                            headers = {"Authorization": "Basic " + self.base_64})

    print("Token refreshed")
    return response.json()["access_token"]



def get_secret_info(info:str) -> str:
    print(__name__)
    print(secrets_path)


get_secret_info("sds")