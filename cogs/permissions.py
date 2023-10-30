import discord
from core import botbase
from discord.ext import commands
from core.helper import interactive_menu as im

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
        req = f"Insert the permission level want: \n * {f'{workaround}* '.join([name.name for name in conf.Permissions])}"
        string_level = await im.request_string(self.bot, channel, member, req)

        try:
            level = conf.Permissions[string_level].value
        except KeyError:
            await self.bot.responses.send(channel, content="This was not a valid option")
            return

        # write to json
        # caching results in dataclass?
        # autosaving
        # decorator checks json or dataclass?


async def setup(bot):
    await bot.add_cog(Permissions(bot))