import enum
from . import colors


class MessageConfig(enum.Enum):
    DEFAULT_COLOR = colors.RED


# colour themes
class ThemeBlue(enum.Enum):
    PRIMARY = "1266FF"
    LLIGHT = "6097FD"
    LIGHT = "347CFF"
    DARK = "0056F4"
    DDARK = "013DAA"


class ViewConfig(enum.Enum):
    pass


def get_color(color: str):
    return int(color, base=16)
