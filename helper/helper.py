import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=Singleton):
    _logger = None
    dev_mode: bool = False

    def __init__(self, path: Path = Path("logs/"), dev_mode: bool = False):
        self.dev_mode = dev_mode

        self.path = path
        filename = path.joinpath("geoffrey.log")
        filename.parent.mkdir(exist_ok=True)
        filename.touch(exist_ok=True)

        self.formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')
        self.handler = TimedRotatingFileHandler(filename, when="midnight", encoding="utf-8")
        self.handler.setFormatter(self.formatter)

        self._logger = logging.getLogger("Logger")
        self._logger.addHandler(self.handler)

        if self.dev_mode:
            self.level = logging.INFO
        else:
            self.level = logging.WARNING

        self._logger.setLevel(self.level)

    def get_logger(self, name: str = ""):
        l = logging.getLogger(name)
        l.addHandler(self.handler)
        l.setLevel(self.level)
        return l


if __name__ == "__main__":
    l = Logger()


