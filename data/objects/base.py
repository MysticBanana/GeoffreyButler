from typing import Dict, Any, Optional, Callable


class BaseObject:

    __slots__ = tuple()

    def __init__(self, *args, **kwargs):
        pass

    def jsonify(self) -> Dict:
        # todo might need a rework
        data = {}
        for i in list(map(lambda x: {x: getattr(self, x)}, self.__slots__)):
            for k, v in i.items():
                data[k] = v if not hasattr(v, "jsonify") else v.jsonify()
        return data

    @staticmethod
    def from_dict(data: dict) -> "BaseObject":
        return BaseObject(**data)
