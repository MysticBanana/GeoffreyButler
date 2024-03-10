import discord
from discord._types import ClientT
from discord.ext import commands, tasks
from discord.ext.commands import Context
from typing import NoReturn
from discord import app_commands

from .config import ACTIVITY_XP, EXTENSION_NAME

from data import db, db_utils

from core.botbase import Bot, BotBase
from discord import ui
import typing

from core.messages import embeds
from . import progressbar

from core.permissions.decorators import has_custom_permission
from core.permissions import conf
import math
from typing import Union


# extension_structure = {
#     "channel_listened": [...],
#     "voice_counts": 0,
#     "attachments": 0
# }

class ChannelSelect(ui.ChannelSelect):
    def __init__(self, bot: BotBase, guild: discord.Guild, *args, **kwargs):
        self.bot = bot

        super().__init__(
            channel_types=[discord.ChannelType.text],
            placeholder="Select channel to count xp",
            min_values=1,
            max_values=5,
            *args,
            **kwargs
        )

    async def callback(self, interaction: discord.Interaction[ClientT]) -> ...:
        await interaction.response.defer()

        channels: typing.List[discord.TextChannel] = []
        for channel_id in interaction.data.get("values", []):
            channels.append(await interaction.guild.fetch_channel(channel_id))

        nl = "\n"
        await interaction.followup.send(f"Following channels will b"
                                        f"e tracked now: {''.join(nl + '* ' + i.mention for i in channels)}",
                                        ephemeral=True)

        server_extension = db_utils.ServerExtension(self.bot, extension_name=EXTENSION_NAME)
        await server_extension.set(guild_id=interaction.guild_id, data={
            "tracked_channel": [i.id for i in channels]
        })


class SetupView(ui.View):
    interaction: discord.Interaction = None
    message: discord.Message = None

    def __init__(self, bot: BotBase, user: Union[discord.User, discord.Member], guild: discord.Guild, timeout: float = 60.0) -> None:
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.guild = guild

        self.add_item(ChannelSelect(self.bot, self.guild))

    async def interaction_check(self, interaction: discord.Interaction[discord.Client]) -> bool:
        if interaction.user.id != self.user.id:
            await interaction.response.send_message(
                "You cannot interact with this view.", ephemeral=True
            )
            return False
            # update the interaction attribute when a valid interaction is received
        self.interaction = interaction
        return True

    async def on_timeout(self) -> None:
        # this method is called when the period mentioned in timeout kwarg passes.
        # we can do tasks like disabling buttons here.
        for button in self.children:
            button.disabled = True  # type: ignore
        # and update the message with the update View.
        if self.message:
            await self.message.edit(view=self)

    async def on_error(
            self, interaction: discord.Interaction[discord.Client], error: Exception,
            item: discord.ui.Item[typing.Any]
    ) -> None:
        # tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        message = f"An error occurred while processing the interaction for [ActivitySetupView]:\n```py\n{error}\n```"
        Bot._logger.get_logger("Activity").warning(message)
        await interaction.response.send_message(message, ephemeral=True)


class ActivityCog(commands.Cog, name="activities"):
    def __init__(self, bot):
        self.bot: BotBase = bot
        self.check_user_in_voice.start()

        self.bot.add_listener(self.on_message, "on_message")

    def cog_unload(self) -> None:
        self.check_user_in_voice.cancel()

    @commands.hybrid_command(name="setup_activity", description="Menu to configure activities")
    @has_custom_permission(name=conf.PermissionType.ADMIN)
    async def setup(self, ctx: Context):
        view = SetupView(self.bot, ctx.author, ctx.guild)

        await self.bot.responses.send(channel=ctx.channel,
                                      view=view,
                                      embed=embeds.build_embed(
                                          author=ctx.author,
                                          title="Acitvity Setup",
                                          description="In this menu you can change the way how this bot collects your"
                                                      "activity data."
                                                      "\n\n"
                                                      "Select a channel where the bot will count messages with an "
                                                      "attachment (e.g. pictures)."
                                                      "\n*Note: If you can't see your channel"
                                                      "type in the first letters and it will appear*"
                                      ))

    @commands.hybrid_command(name="status", description="Shows the user status")
    async def status(self, ctx: Context):

        user = await db_utils.fetch_user(ctx.guild.id, ctx.author.id)

        max_xp = 400
        await self.bot.responses.send(channel=ctx.channel,
                                      embed=embeds.build_embed(
                                          author=ctx.author,
                                          title="Activity Status",
                                          description=f"**Level: {int(math.floor(user.xp)/max_xp) + 1}**\n"
                                                      f"**XP: {user.xp}**\n"
                                                      f"```{progressbar.Bar(max_xp, user.xp % max_xp, 20).get_bar()}```"
                                      ))

    @tasks.loop(minutes=5)
    async def check_user_in_voice(self) -> NoReturn:
        """
        Does a check every 5 minutes. Each player in a call gets a specific amount of xp
        """

        for guild in self.bot.guilds:
            voice_channels = guild.voice_channels

            for vc in voice_channels:
                if len(vc.voice_states) != 0:
                    for user_id, state in vc.voice_states.items():
                        await add_xp(guild.id, user_id, ACTIVITY_XP.voice)

    @check_user_in_voice.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()

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

    async def on_message(self, message: discord.Message):
        if not message.author.bot and message.attachments:
            channel_ids = await db_utils.ServerExtension.fast_fetch(EXTENSION_NAME, message.guild.id, "tracked_channel")

            if message.channel.id in channel_ids:
                # todo this might need to get cached to avoid alot traffic
                await add_xp(message.guild.id, message.author.id, ACTIVITY_XP.attachment)


async def add_xp(guild_id: int, user_id: int, xp: int) -> NoReturn:
    user = await db_utils.fetch_user(guild_id, user_id)

    await db_utils.insert_user(guild_id, user_id, xp=user.xp+xp)


async def setup(bot):
    await bot.add_cog(ActivityCog(bot))
