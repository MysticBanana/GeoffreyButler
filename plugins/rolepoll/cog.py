import discord
from discord.ext import commands
from core import botbase
from core.audio import audiocontroller
from . import config
from core import messages
from core.messages import view_controller
from core import helper
import helper as _helper
from typing import Optional, Tuple, Union, Dict, List
import discord
from . import pollcontroller
from .models import poll


class RolePollCog(commands.Cog):
    def __init__(self, bot: botbase.BotBase):
        self.bot: botbase.BotBase = bot
        self.logger = _helper.Logger().get_logger(self.__class__.__name__)

    @commands.command(name="rp_create", description="creates a category with roles")
    async def create_poll(self, ctx):
        role_controller = self.bot.get_role_controller(ctx.guild)
        extension_controller = self.bot.get_extension_config_handler(ctx.guild, config.EXTENSION_NAME)

        _poll: List[List[int, str, str]] = []

        req = "Insert the title of your poll"
        title = await helper.interactive_menu.request_string(self.bot, ctx.channel, ctx.author, req)

        req = "Insert all available roles"
        roles = await helper.interactive_menu.request_roles(self.bot, ctx.channel, ctx.author, req)

        for role in roles:
            req = f"Insert the displayed name '{role.name}' (insert '#' for none)"
            displayed = await helper.interactive_menu.request_string(self.bot, ctx.channel, ctx.author, req)

            req = emoji = f"Insert the displayed emoji '{role.name}'"
            emoji = await helper.interactive_menu.request_emoji(self.bot, ctx.channel, ctx.author, req)

            _poll.append([role.id, displayed, emoji])

        p = poll.Poll(message_id=0, channel_id=ctx.channel.id, title=title, poll=_poll)

        await pollcontroller.create_poll(self.bot, ctx.guild, ctx.channel, p)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        emoji = str(payload.emoji)
        message_id = payload.message_id
        channel_id = payload.channel_id
        member = payload.member
        guild_id = payload.guild_id

        channel = await self.bot.fetch_channel(channel_id)
        message = await channel.fetch_message(message_id)
        guild = await self.bot.fetch_guild(guild_id)

        if message.content.startswith(pollcontroller.RP_PREFIX):
            self.logger.info(f"adding role to user {member.name} - user_id:{member.id}")
            await pollcontroller.add_reaction(self.bot, guild, channel, message_id, member, emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        emoji = str(payload.emoji)
        message_id = payload.message_id
        channel_id = payload.channel_id
        guild_id = payload.guild_id

        channel = await self.bot.fetch_channel(channel_id)
        message = await channel.fetch_message(message_id)
        guild = await self.bot.fetch_guild(guild_id)
        member: discord.Member = await guild.fetch_member(payload.user_id)

        if message.content.startswith(pollcontroller.RP_PREFIX):
            self.logger.info(f"removing role from user {member.name} - user_id:{member.id}")
            await pollcontroller.remove_reaction(self.bot, guild, channel, message_id, member, emoji)


async def setup(bot):
    await bot.add_cog(RolePollCog(bot))
