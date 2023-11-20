import discord
from core import botbase
from discord.ext import commands
from core.helper import interactive_menu as im
# from core.permissions import Permission
from data import models
from core.permissions.decorators import *


from core.permissions import conf


class Permissions(commands.Cog):
    def __init__(self, bot: botbase.BotBase):
        self.bot: botbase.BotBase = bot

    @commands.command(name="set_role", description="Sets a role to a specific permission level")
    @commands.has_permissions(administrator=True)
    async def set_role(self, ctx):
        channel = ctx.channel
        member = ctx.message.author

        req = "Insert the roles you want to assign"
        roles = await im.request_roles(self.bot, channel, member, req)

        workaround = "\n"
        req = f"Insert the permission level want:" \
              f" \n * {f'{workaround}* '.join([name.name for name in conf.PermissionType])}"
        string_level = await im.request_string(self.bot, channel, member, req)

        try:
            level = conf.PermissionType[string_level.upper()].value
        except KeyError:
            await self.bot.responses.send(channel, content="This was not a valid option")
            return

        permission = models.Permission(role_ids=[role.id for role in roles], level=level)
        guild = self.bot.guilds.get(ctx.guild.id)
        guild.add_permission(permission)
        guild.flush()

        # write to json
        # caching results in dataclass?
        # autosaving
        # decorator checks json or dataclass?

    @commands.command(name="test_permission", description="Sets a role to a specific permission level")
    @has_custom_permission(name=conf.PermissionType.ADMIN)
    async def test_permission(self, ctx):
        print("aye")


async def setup(bot):
    await bot.add_cog(Permissions(bot))