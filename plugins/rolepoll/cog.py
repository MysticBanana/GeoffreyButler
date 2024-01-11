from discord.ext import commands
from typing import List

import discord
import emoji as discord_emoji
from discord.ext import commands

import helper as _helper
from core import botbase
from core import helper
from . import config
from . import pollcontroller
from .models import poll

from core.permissions.decorators import has_custom_permission
from core.permissions import conf


class PollCog(commands.Cog, name="Poll"):
    def __init__(self, bot: botbase.BotBase):
        self.bot: botbase.BotBase = bot
        self.logger = _helper.Logger().get_logger(self.__class__.__name__)

    @commands.cooldown(3, 10)
    @commands.command(name="poll", help="Poll with multiple options", description="Creates a customizable poll with an "
                                                                                  "interactive menu. The user can "
                                                                                  "choose his own emojis or use "
                                                                                  "default (1-10).")
    async def create_simple_poll(self, ctx, channel: discord.TextChannel = None):
        """
        Creates a customizable poll with an interactive menu. The user can choose his own emojis or use default (1-10).

        :param ctx: Context
        :param channel: Channel to send the finished poll
        """

        req = "Insert your poll title"
        title = await helper.interactive_menu.request_string(self.bot, ctx.channel, ctx.author, req)

        req = "How many options should be in the poll"
        options = await helper.interactive_menu.request_int(self.bot, ctx.channel, ctx.author, req)

        req = "Do you want to assign special emoji for each role? (max 10 roles)"
        assign_emoji = await helper.interactive_menu.request_bool(self.bot, ctx.channel, ctx.author, req)

        p = []
        for i in range(options):
            if assign_emoji:
                req = f"Select an emoji for option number {i+1}"
                emoji = await helper.interactive_menu.request_emoji(self.bot, ctx.channel, ctx.author, req)
            else:
                # to many roles
                if i > 9:
                    return
                emoji = discord_emoji.emojize(f":keycap_{i+1}:")

            req = f"Input a description for option number {i+1}"
            option = await helper.interactive_menu.request_string(self.bot, ctx.channel, ctx.author, req)

            p.append((emoji, option))

        p = poll.Poll(None, None, title, p, 1)

        await pollcontroller.simple_poll(self.bot, ctx.guild, channel or ctx.channel, p)
        await ctx.message.delete()

    @commands.cooldown(3, 10)
    @commands.command(name="shortpoll", help="Poll with 2 options", description="Creates a simple poll with "
                                                                                "`thump up/down` reaction.")
    async def create_short_poll(self, ctx, channel: discord.TextChannel = None):
        """
        Creates a simple poll with `thump up/down` reaction.

        :param ctx: Context
        :param channel: Channel to send the finished poll
        """

        req = "Insert your poll title"
        title = await helper.interactive_menu.request_string(self.bot, ctx.channel, ctx.author, req)

        p = poll.Poll(None, None, title, [("👍",), ("👎",)], 1)

        await pollcontroller.title_poll(self.bot, ctx.guild, channel or ctx.channel, p)
        await ctx.message.delete()

    @commands.cooldown(3, 10)
    @commands.command(name="rp_create", help="Poll to assign roles", description="Creates a customizable role poll with"
                                                                                 " an interactive menu. The user can "
                                                                                 "choose his own emojis or use "
                                                                                 "default (1-10).")
    @has_custom_permission(name=conf.PermissionType.MODERATOR)
    async def create_poll(self, ctx, channel: discord.TextChannel = None):
        """
        Creates a customizable role poll with an interactive menu. The user can choose his own emojis or use
        default (1-10).

        :param ctx: Context
        :param channel: Channel to send the finished poll
        """

        role_controller = self.bot.get_role_controller(ctx.guild)
        extension_controller = self.bot.get_extension_config_handler(ctx.guild, config.EXTENSION_NAME)

        _poll: List[List[str, str, int]] = []

        req = "Insert the title of your poll"
        title = await helper.interactive_menu.request_string(self.bot, ctx.channel, ctx.author, req)

        req = "Insert all available roles"
        roles = await helper.interactive_menu.request_roles(self.bot, ctx.channel, ctx.author, req)

        req = "Do you want to assign special emoji for each role? (max 10 roles)"
        assign_emoji = await helper.interactive_menu.request_bool(self.bot, ctx.channel, ctx.author, req)

        for num, role in enumerate(roles):
            req = f"Insert the displayed name '{role.name}' (insert '-' for none)"
            displayed = await helper.interactive_menu.request_string(self.bot, ctx.channel, ctx.author, req)

            if assign_emoji:
                req = f"Insert the displayed emoji '{role.name}'"
                emoji = await helper.interactive_menu.request_emoji(self.bot, ctx.channel, ctx.author, req)
            else:
                # to many roles
                if num > 9:
                    return
                emoji = discord_emoji.emojize(f":keycap_{num+1}:")

            _poll.append([emoji, displayed, role.id])

        p = poll.Poll(message_id=0, channel_id=ctx.channel.id, title=title, poll=_poll)

        await pollcontroller.create_poll(self.bot, ctx.guild, channel or ctx.channel, p)
        await ctx.message.delete()

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
    await bot.add_cog(PollCog(bot))
