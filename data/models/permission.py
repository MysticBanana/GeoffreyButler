import discord.guild
from typing import Dict, Any, Optional, List, Set, Union
from data import ConfigHandler, ExtensionConfigHandler
from . import base
from . import user
from . import role
from core.permissions import conf

from collections import defaultdict


class Permission(base.BaseObject):
    role_id: int = None
    role_ids: Set[int] = []
    level: int = 0

    def __init__(self, role_id: int = None, role_ids: Union[Set[int], List[int]] = None, level: int = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if role_id is not None:
            self.role_ids.add(role_id)
        else:
            self.role_ids = set(role_ids)

        self.level = level

    def jsonify(self):
        return {
            "role_ids": list(self.role_ids),
            "level": self.level
        }

    @staticmethod
    def from_dict(**data: dict) -> "Permission":
        return Permission(**data)


class Permissions(base.BaseObject):
    permissions: Dict[int, Permission]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.permissions = {}
        if len(kwargs) == 0:
            return

        for k, permission_data in kwargs.items():
            self.permissions[int(k)] = Permission.from_dict(**permission_data)

    def has_permission(self, permission: conf.PermissionType, role: discord.Role) -> bool:


        for level, perm in self.permissions.items():

            if role.id in perm.role_ids:
                if permission.value <= level:
                    return True

        return False

    def add_permission(self, permission: Permission):
        perm = self.permissions.get(permission.level)

        if perm is None:
            self.permissions[permission.level] = permission
            return

        perm.role_ids = perm.role_ids | permission.role_ids

    def jsonify(self) -> Dict[str, Dict]:
        return {perm.level: perm.jsonify() for perm in self.permissions.values()}

    @staticmethod
    def from_dict(data: List[Any]) -> "Permissions":
        return Permissions(**data)
