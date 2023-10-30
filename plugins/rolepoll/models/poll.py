from typing import Tuple, List, Dict, Union, Callable, Any, Optional
import discord
import hashlib


class Poll:
    _id: str
    _message_id: int
    _channel_id: int
    _options: List[List[Union[int, str]]]
    _title: str

    def __init__(self, message_id: int, channel_id: int, title: str, poll: List[Any], id: str  = 0):
        self._message_id = message_id
        self._channel_id = channel_id
        self._title = title
        self._options = []

        self._id = id if id != 0 else str(hashlib.sha1(str(poll).encode("utf-8")).hexdigest())

        for role in poll:
            self._options.append(role)

    @property
    def emojis(self) -> List[str]:
        emojis = []
        for para in self._options:
            emojis.append(para[0])

        return emojis

    @property
    def message_id(self) -> int:
        return self._message_id

    @message_id.setter
    def message_id(self, value):
        self._message_id = value

    @property
    def channel_id(self) -> int:
        return self._channel_id

    @property
    def title(self):
        return self._title

    @property
    def param(self):
        return self._options

    @staticmethod
    def from_dict(data: Dict[str, List[Union[int, str, List[Union[int , str]]]]]) -> "Poll":
        id = list(data.keys())[0]
        message_id, channel_id, title, data = list(data.values())

        return Poll(message_id, channel_id, title, data, id)

    def jsonify(self) -> Dict[str, List[Union[int, str, List[Union[int , str]]]]]:
        return {self._id: [self._message_id, self._channel_id, self._title] + self._options}

