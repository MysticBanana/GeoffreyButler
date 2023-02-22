from typing import Optional, Tuple, Union, Dict, List, Any
import discord


class Addon:
    _id: int
    _notify: bool
    _channel_id: int
    _role_id: int

    def __init__(self, id: int, notify: bool = False, channel_id: int = None, role_id: int = None, **kwargs):
        self._id = id
        self._notify = notify
        self._channel_id = channel_id
        self._role_id = role_id

    @staticmethod
    def from_dict(**kwargs) -> "Addon":
        return Addon(**kwargs)

    def jsonify(self) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "notify": self._notify,
            "channel_id": self._channel_id,
            "role_id": self._role_id
        }

        return {str(self._id): data}

    @property
    def id(self):
        return self._id

    @property
    def channel_id(self):
        return self._channel_id

    @property
    def role_id(self):
        return self._role_id