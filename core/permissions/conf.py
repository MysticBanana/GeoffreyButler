import enum

class PermissionType(enum.Enum):
    BASE = 0
    EXTENDED = 1
    MODERATOR = 2
    ADMIN = 3