import enum
from typing import Optional, Tuple, Union, Dict, List
from . import colors, embeds, message_config, exceptions
import discord
from discord.ui import Button, View


class MessageController:

    config: message_config.MessageConfig

    def __init__(self, bot, guild: discord.Guild = None, config: message_config.MessageConfig = message_config.MessageConfig):
        self.bot = bot
        self.guild = guild
        self.config = config

    def get_color(self, color: str):
        return int(color, base=16)

    async def add_reaction(self, message: discord.Message, reactions: List[str] = None, reaction: str = None):
        reactions = [] if reactions is None else reactions

        if reaction:
            reactions.append(reaction)

        for _reaction in reactions:
            await message.add_reaction(_reaction)

    def build_embed(self, **kwargs) -> discord.Embed:
        embed: discord.Embed = embeds.build_embed(**kwargs)
        return embed

    async def send(self, channel: discord.TextChannel = None, channel_id: int = None, embed: discord.Embed = None,
                   content: str = None, title: str = None, reactions: List[str] = None, make_embed: bool = True,
                   view: View = None, **kwargs) -> discord.Message:

        """
        :param channel: channel to send to
        :param channel_id: if channel is none fetches channel from id
        :param embed: embed to send
        :param content: text to send or if `make_embed` content of the embed
        :param title: title of the embed
        :param reactions: reactions that are added to the message
        :param make_embed: automatically converts given text into an embed
        :param view: view that will be added to the message
        """

        if channel is None:
            if not channel_id:
                raise exceptions.MissingChannelId("Cant send a message without a given Channel or Channel_Id")

            channel = await self.bot.fetch_channel(channel_id)

        if embed is None and make_embed:
            embed = self.build_embed(description=content, title=title, **kwargs)

        if embed is not None:
            message = await channel.send(embed=embed, view=view)
        else:
            message = await channel.send(content=content, view=view)

        await self.add_reaction(message, reactions)

        return message
