import enum
from . import colors


class MessageConfig(enum.Enum):
    DEFAULT_COLOR = colors.CYAN


class ViewConfig(enum.Enum):
    pass


def get_color(color: str):
    return int(color, base=16)
