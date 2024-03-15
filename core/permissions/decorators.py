from typing import *
from core.permissions import conf
from discord.ext.commands import Context
from discord.ext.commands import check as check_predicate
from .. import bot as _bot
from data import db, db_utils
import asyncio


def has_custom_permission(*args, **kwargs):
    name = kwargs.get("name")

    async def predicate(ctx: Context) -> bool:

        if name.value == 0:
            return True

        if ctx.author.guild_permissions.administrator:
            return True

        roles = ctx.author.roles
        guild = ctx.guild

        guild_data = await db_utils.fetch_guild(guild_id=guild.id)
        permissions = guild_data.permissions

        for role in roles:
            for level, perm in permissions.items():
                if name.value <= int(level):
                    if role.id in perm:
                        return True
        return False
    return check_predicate(predicate)