from typing import Optional, Tuple, Union, Dict, List
from discord import Role as _Role


class Role:
    _id: int
    _name: str

    @staticmethod
    def from_role(role: _Role) -> "Role":
        pass

    def dump(self):
        pass
