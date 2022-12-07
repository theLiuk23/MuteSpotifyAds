from settings import Settings
from requests import post
from datetime import datetime
import sys


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
        if (t1 - t0).total_seconds() >= 3600:
            return False
        return True


    # returns valid token to main2.py
    def return_token(self) -> str:
        if not self.verify_login():
            self.refresh()
        return self.old_token


    # gets brand new token
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