from . import addon
from typing import Optional, Tuple, Union, Dict, List, Any


class Game:
    _id: int
    _addons: Dict[int, addon.Addon]

    def __init__(self, id: int, addons: Dict[int, addon.Addon] = None, **kwargs):
        self._id = id
        self._addons = addons or {}

    def add_addon(self, _addon: addon.Addon):
        self._addons.update({_addon.id: _addon})

    def jsonify(self) -> Dict[str, Union[str, Dict[int, Any]]]:
        data = {str(self.game_id): {}}

        for _id, _addon in self._addons.items():
            data[str(self._id)].update(_addon.jsonify())

        return data

    def from_dict(self, **kwargs) -> "Game":
        return Game(kwargs.get("id"), kwargs.get("addons"))

    @property
    def game_id(self):
        return self._id

    @property
    def addons(self) -> Dict[int, addon.Addon]:
        return self._addons