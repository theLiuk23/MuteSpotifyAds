class OsNotSupported(BaseException):
    def __init__(self, msg:str):
        super().__init__()