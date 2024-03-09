from typing import Tuple, List, Dict, Union, Callable, Any, Optional
import discord
import hashlib


class Poll:
    _options: List[List[Union[int, str]]]
    _title: str

    def __init__(self, title: str, poll: List[Any]):
        self._title = title
        self._options = []

        for role in poll:
            self._options.append(role)

    def get_role_by_emoji(self, emoji: str) -> int:
        for i, em in enumerate(self.emojis):
            if em == emoji:
                return self.param[i][2]

    @property
    def emojis(self) -> List[str]:
        emojis = []
        for para in self._options:
            emojis.append(para[0])

        return emojis

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value

    @property
    def param(self):
        return self._options

    @param.setter
    def param(self, value: List):
        self._options = value

    @staticmethod
    def from_dict(data: Dict[str, List[Union[int, str, List[Union[int , str]]]]]) -> "Poll":
        d = next(data.values().__iter__()).copy()
        title = d.pop(0)

        return Poll(title, d)

    def jsonify(self) -> List[Any]:
        return [self._title] + self._options

