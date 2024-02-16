import logging
from logging.handlers import TimedRotatingFileHandler
from logging import StreamHandler
from pathlib import Path
import sys

logger: "Logger" = None


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger:
    logger: logging.Logger = None
    dev_mode: bool = False

    def __init__(self, path: Path = Path("logs/"), filename: str = "geoffrey.log", dev_mode: bool = False):
        self.dev_mode = dev_mode
        self.path = path

        filename = path / filename
        filename.parent.mkdir(exist_ok=True)
        filename.touch(exist_ok=True)

        self.formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')
        self.time_handler = TimedRotatingFileHandler(filename, when="midnight", encoding="utf-8")
        self.time_handler.setFormatter(self.formatter)

        self.console_handler = StreamHandler(stream=sys.stdout)
        self.console_handler.setFormatter(self.formatter)

        self.error_handler = StreamHandler(stream=sys.stderr)
        self.error_handler.setFormatter(self.formatter)
        self.error_handler.setLevel(logging.ERROR)

        self.logger = self.get_logger("Main")

    def get_logger(self, name):
        log = logging.getLogger(name)

        if self.dev_mode:
            self.console_handler.setLevel(logging.DEBUG)
            self.time_handler.setLevel(logging.INFO)

            log.addHandler(self.console_handler)
            log.addHandler(self.time_handler)

        else:
            self.time_handler.setLevel(logging.WARNING)
            log.addHandler(self.error_handler)
            log.addHandler(self.time_handler)

        return log