import dataclasses


class Action:
    _id: int
    name: str

    @property
    def id(self):
        return self._id


class Event:
    _id: int
    name: str

    action: Action

    @property
    def id(self):
        return self._id


class ReactionEvent(Event):
    pass


class Channel:
    _id: int
    name: str

    events: list

    allowed_roles: list
    denied_roles: list

    @property
    def id(self):
        return self._id


class RoleAction(Action):
    """
    Role management through Action
    """

    def __init__(self):
        pass

    @property
    def id(self):
        return


if __name__ == "__main__":
    a = RoleAction()
    print(a)




