from dataclasses import dataclass

import discord.guild
from typing import Dict, Any, Optional, List
from data import ConfigHandler, ExtensionConfigHandler
from . import base
from . import user
from . import role

from collections import defaultdict


class GuildData(base.BaseObject):
    guild_id: int
    name: str

    users: Dict[int, Any]
    roles: role.Roles

    # used to store extension specific data
    extension: Dict[str, Any]

    __slots__ = ("guild_id", "name", "users", "extension", "roles")

    def __init__(self, guild_id, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.guild_id = guild_id
        self.name = name

        self.users = kwargs.get("users", {})
        self.extension = kwargs.get("extension", {})
        self.roles = kwargs.get("roles")
        self.roles = role.Roles.from_dict(self.roles) if self.roles is not None else role.Roles()

    def get_extension_data(self, extension_name: str) -> Optional[dict]:
        return self.extension.get(extension_name)

    def set_extension_data(self, extension_name: str, data: dict):
        self.extension[extension_name] = data

    @staticmethod
    def from_dict(data: dict) -> "GuildData":
        return GuildData(**data)


class Guild:
    guild_data: GuildData

    def __init__(self, bot, guild_id: int = None, name: str = None, guild_data: GuildData = None, **kwargs):
        self.bot = bot
        self.guild_data = guild_data if guild_data is not None else GuildData(guild_id, name, **kwargs)

        self.config_handler = ConfigHandler(bot, self)

    def __getitem__(self, item):
        pass

    def __setitem__(self, key, value):
        pass

    def __getattr__(self, item):
        if self.guild_data is not None:
            if hasattr(self.guild_data, item):
                return getattr(self.guild_data, item)

        raise AttributeError

    def get_role(self, *, id: int) -> role.Role:
        return self.guild_data.roles.get_role(id=id)

    def add_role(self, *, role: discord.Role):
        self.guild_data.roles.add_role(role=role)

    def remove_role(self, *, role: discord.Role = None, id: int = None):
        self.guild_data.roles.remove_role(role=role, id=id)

    def register_extension_config_handler(self, extension_name) -> ExtensionConfigHandler:
        if extension_name not in self.config_handler.extension_handler:
            self.config_handler.extension_handler[extension_name] = ExtensionConfigHandler(self.config_handler, extension_name)

        return self.config_handler.extension_handler.get(extension_name)

    def jsonify(self) -> Dict:
        if self.guild_data is not None:
            return self.guild_data.jsonify()
        else:
            return {}

    def get(self, key, *args):
        pass

    def flush(self):
        self.config_handler.flush()

    @staticmethod
    def from_guild(bot, guild: discord.guild.Guild) -> "Guild":
        return Guild(bot, guild.id, guild.name)

    @staticmethod
    def from_guild_id(bot, guild_id: int) -> "Guild":
        data = ConfigHandler.guild_data_from_id(bot, guild_id)

        return Guild.from_dict(bot, data)

    @staticmethod
    def from_dict(bot, data: dict) -> "Guild":
        try:
            return Guild(bot, guild_data=GuildData(**data))
        except Exception as e:
            raise e


