class OsNotSupported(BaseException):
    def __init__(self, *args):
        super().__init__()