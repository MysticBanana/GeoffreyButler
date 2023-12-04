from typing import *
from core.permissions import conf
from discord.ext.commands import Context
from discord.ext.commands import check as check_predicate
from .. import bot as _bot


def has_custom_permission(*args, **kwargs):
    name = kwargs.get("name")

    # if type(name) == str:
    #     name = conf.PermissionType[name.upper()]

    def predicate(ctx: Context) -> bool:

        if name.value == 0:
            return True

        roles = ctx.author.roles
        guild = ctx.guild
        _guild = _bot.Geoffrey.instance.guilds.get(guild.id)

        for role in roles:
            if _guild.check_permission(name, role):
                return True

        return False

    return check_predicate(predicate)