from dataclasses import dataclass, field
from typing import *


@dataclass()
class Permission:
    role_id: int = None
    role_ids: List[int] = field(default_factory=list)
    level: int = 0

    def __post_init__(self):
        if self.role_id is not None:
            self.role_ids.append(self.role_id)

    def jsonify(self):
        return {
            "roles": self.role_ids,
            "level": self.level
        }


class Permissions:
    bot: object

    def __init__(self, bot):
        self.bot = bot

    def add_permission(self, permission: Permission):
        pass

