from configparser import RawConfigParser
from datetime import datetime
from requests import post
import os


# called from main.py
# it checks if the old token has expired (older than 1h)
# if it is, a new token will be generated
def verify_login() -> str:
    last_time = get_info(data_path, "data", "last_time_token_refreshed")
    t0 = datetime.strptime(last_time, time_format)
    t1 = datetime.now()
    print(t0, " - ", t1)
    if (t1 - t0).total_seconds() >= 3600:
        return refresh()
    return refresh_token


def refresh() -> str:
    '''gets brand new token ready to use'''
    response = post(url = "https://accounts.spotify.com/api/token",
                    data = {"grant_type":"refresh_token",
                                    "refresh_token": refresh_token},
                    headers = {"Authorization": "Basic " + base_64})

    # if access_token is in the response, the new token will be sent to main.py
    if "access_token" in response.json():
        print("Token refreshed")
        return response.json()["access_token"]
    # if old token was still valid, it will be sent to main.py
    return refresh_token


# gets a value from secrets.ini or data.ini
def get_info(path:str, section:str, info:str) -> str:
    config.read(path)
    return config.get(section, info)


# sets a value in secrets.ini or data.ini
def set_info(path:str, section:str, info:str, value):
    with open(path, "w") as file:
        config.set(section, info, str(value))
        config.write(file)



config = RawConfigParser()
time_format = r"%Y-%m-%d %H:%M:%S"
secrets_path = os.path.dirname(__file__) + "/secrets.ini"
data_path = os.path.dirname(__file__) + "/data.ini"
base_64 = get_info(secrets_path, "secrets", "base_64")
refresh_token = get_info(secrets_path, "secrets", "refresh_token")