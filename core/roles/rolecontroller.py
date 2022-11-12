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

    def load_roles(self):
        pass

    def add_role(self, *, role: discord.Role):
        self.bot.GUILDS[self.guild.id].add_role(role=role)

