class OsNotSupported(BaseException):
    def __init__(self, msg:str):
        super().__init__()
        if msg:
            print(msg)