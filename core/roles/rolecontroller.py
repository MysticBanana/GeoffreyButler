from typing import Tuple, List, Dict, Union, Callable, Any
import discord


class RoleController:

    controller: Dict[discord.Guild, "RoleController"] = {}
    guild: discord.Guild

    def __init__(self, bot, guild: discord.Guild):
        self.bot = bot
        self.guild = guild
        self.controller[guild] = self

    def __new__(cls, *args, **kwargs):
        guild = kwargs.get("guild", None) or args[1]
        if guild in cls.controller:
            return cls.controller.get(guild)

        return super(RoleController, cls).__new__(cls)

    def add_role(self, *, role: discord.Role):
        self.bot.GUILDS[self.guild.id].add_role(role=role)

    def remove_role(self, *, role: discord.Role = None, id: int = None):
        self.bot.GUILDS[self.guild.id].remove_role(role=role, id=id)

    def get_role_by_id(self, id: int):
        return self.guild_data.get_role(id=id)

    def get_role_by_role(self, role: discord.Role):
        return self.guild_data.get_role(id=role.id)

    def get_data(self, *, role: discord.Role = None, id: int = None):
        pass

    def set_data(self, *, role: discord.Role = None, id: int = None):
        pass

    def add_data(self, *, role: discord.Role = None, id: int = None):
        pass

    @property
    def guild_data(self):
        return self.bot.GUILDS[self.guild.id]

