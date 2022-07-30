class GeoffreyException(Exception):
    message: str = ""
    output = "{}: {}"

    def __init__(self, message: str = ""):
        self.message = message

    def __str__(self):
        return self.output.format(self.__class__.__name__, self.message)
