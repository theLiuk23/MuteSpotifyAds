from configparser import RawConfigParser
import os


secrets_path = os.path.dirname(__file__) + "/secrets.ini"
data_path = os.path.dirname(__file__) + "/data.ini"


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