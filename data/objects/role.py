from typing import Dict, Any, Optional, List, Set
from . import base
import discord


class Role(base.BaseObject):

    id: int
    name: str
    data: List

    __slots__ = ("id", "name", "data")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = kwargs.get("id")
        self.name = kwargs.get("name")

        self.data = kwargs.get("data", [])

    @staticmethod
    def from_dict(data: Dict) -> "Role":
        return Role(**data)

    @staticmethod
    def from_discord(role: discord.Role):
        return Role(id=role.id, name=role.name, role=role)

    def __hash__(self):
        return self.id


class Roles(base.BaseObject):

    roles: Set[Role]

    __slots__ = ("roles",)

    def __init__(self, *roles, **kwargs):
        super().__init__(*roles, **kwargs)

        self.roles = set()

        for role in roles:
            self.roles.add(Role.from_dict(role))

    def add_role(self, *, role: discord.Role):
        self.roles.add(Role.from_discord(role))

    def get_role(self, *, id: int):
        for role in self.roles:
            if role.id == id:
                return role

    def jsonify(self) -> List[Dict]:
        return [role.jsonify() for role in self.roles]

    @staticmethod
    def from_dict(data: List[Any]) -> "Roles":
        return Roles(*data)


