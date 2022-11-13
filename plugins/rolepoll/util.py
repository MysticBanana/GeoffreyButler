from typing import Tuple, List, Dict, Union, Callable, Any
import discord


class Category:

    category_name: str
    roles: Dict[int, str] # id: description

    def __init__(self, category_name, roles: Dict[int, str]):

        self.category_name = category_name
        self.roles = roles

    def jsonify(self):
        return {self.category_name: self.roles}

    def from_dict(self, **data: Dict[str, Dict[int, str]]):
        if len(data) == 0:
            return
        cat = list(data.values())[0]
        return Category(cat, data[cat])

