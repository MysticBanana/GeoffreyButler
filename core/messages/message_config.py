import enum
from . import colors


class MessageConfig(enum.Enum):
    DEFAULT_COLOR = colors.CYAN


def get_color(color: str):
    return int(color, base=16)
