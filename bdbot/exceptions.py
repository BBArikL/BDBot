class ComicNotFound(BaseException):
    def __init__(self, message, comic_name: str | None = None):
        super().__init__(message)
        self.message = message
        self.comic_name = comic_name
