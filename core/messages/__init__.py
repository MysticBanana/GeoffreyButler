from .messages import MessageController, controller
from . import view_controller
from . import embeds
from . import colors
from . import views

from discord import TextChannel, Embed, Message
from discord.ext import commands


async def send(channel: TextChannel, content: str = "", embed: Embed = None) -> Message:
    """
    Sends a message in a given channel

    :param channel: Discord TextChannel
    :param content: Normal string message you want to send
    :param embed: Send embed instead of content
    :return: Message send
    """
    return await controller.send(channel, content=content)


async def respond(reference: Message, content: str = "", embed: Embed = None) -> Message:
    """
    Sends a response on a message referencing a message

    :param reference: Message you want to reference
    :param content: Normal string message you want to send
    :param embed: Send embed instead of content
    :return: Message send
    """
    return await reference.channel.send(content=content, embed=embed, reference=reference)
