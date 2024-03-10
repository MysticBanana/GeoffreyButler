import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from logging import StreamHandler
import sys


log: "Logger" = None


class Logger:
    logger: logging.Logger = None
    dev_mode: bool = False

    def __init__(self, path: Path = Path("logs/"), filename: str = "geoffrey.log", dev_mode: bool = False):
        self.dev_mode = dev_mode
        self.path = path

        filename = path / filename
        filename.parent.mkdir(exist_ok=True)
        filename.touch(exist_ok=True)

        dt_fmt = '%Y-%m-%d %H:%M:%S'
        self.formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s', dt_fmt)
        self.time_handler = TimedRotatingFileHandler(filename, when="midnight", encoding="utf-8")
        self.time_handler.setFormatter(self.formatter)

        self.console_handler = StreamHandler(stream=sys.stdout)
        self.console_handler.setFormatter(self.formatter)

        self.error_handler = StreamHandler(stream=sys.stderr)
        self.error_handler.setFormatter(self.formatter)
        self.error_handler.setLevel(logging.ERROR)

        log = self

    @property
    def file_handler(self) -> TimedRotatingFileHandler:
        return self.time_handler

    @property
    def stream_handler(self) -> StreamHandler:
        return self.console_handler

    def get_logger(self, name):
        log = logging.getLogger(name)

        if self.dev_mode:
            self.console_handler.setLevel(logging.DEBUG)
            self.time_handler.setLevel(logging.INFO)

            log.addHandler(self.console_handler)
            log.addHandler(self.time_handler)

            log.setLevel(logging.DEBUG)

        else:
            self.time_handler.setLevel(logging.WARNING)
            log.addHandler(self.error_handler)
            log.addHandler(self.time_handler)

            log.setLevel(logging.INFO)
        return log


if __name__ == "__main__":
    l = Logger()
