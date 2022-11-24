import requests




def verify_login():
    pass



def refresh(self):
    '''gets brand new token ready to use'''
    response = requests.post(url = "https://accounts.spotify.com/api/token",
                            data = {"grant_type":"refresh_token",
                                    "refresh_token": self.refresh_token},
                            headers = {"Authorization": "Basic " + self.base_64})

    print("Token refreshed")
    self.old_token = response.json()["access_token"]



def get_secret_info(info:str) -> str:
    