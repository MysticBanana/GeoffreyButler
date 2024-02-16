from typing import Tuple, List, Dict, Union, Callable, Any, Optional
import discord
from . import config
from .models import poll


RP_PREFIX = "**RolePoll - "


async def cleanup(bot, guild: discord.Guild):
    extension_controller = bot.get_extension_config_handler(guild, config.EXTENSION_NAME)

    for id, _poll in extension_controller.data.items():
        p = poll.Poll.from_dict({id: _poll})

        try:
            message = bot.fetch_channel(p.channel_id).fetch_message(p.message_id)
        except discord.NotFound:
            message = None

        if message is None:
            extension_controller.remove(id)


async def simple_poll(bot, guild: discord.Guild, channel: discord.TextChannel, p: poll.Poll):
    content = f"**{p.title}**\n\n"

    for option in p.param:
        _emoji, description = option

        content += f"{_emoji} - {description}\n"

    await bot.responses.send(channel=channel, make_embed=False, content=content, reactions=p.emojis)


async def title_poll(bot, guild: discord.Guild, channel: discord.TextChannel, p: poll.Poll):
    await bot.responses.send(channel=channel, make_embed=False, content=f"{p.title}", reactions=p.emojis)


async def create_poll(bot, guild: discord.Guild, channel: discord.TextChannel, _poll: poll.Poll):
    role_controller = bot.get_role_controller(guild)
    extension_controller = bot.get_extension_config_handler(guild, config.EXTENSION_NAME)

    content = format_poll(guild, _poll)

    # sending messages
    msg: discord.Message = await bot.responses.send(channel=channel, make_embed=False, content=content, reactions=_poll.emojis)
    _poll.message_id = msg.id

    extension_controller.update(_poll.jsonify())
    extension_controller.flush()

async def modify_poll(bot, guild: discord.Guild, channel: discord.TextChannel, reference: discord.MessageReference,
                      _poll: poll.Poll):
    extension_controller = bot.get_extension_config_handler(guild, config.EXTENSION_NAME)
    content = format_poll(guild, _poll)

    # message = channel.fetch_message(reference.message_id)
    # todo how to getch the message correctly
    message: discord.Message = await bot.fetch_message(reference.message_id)
    await message.edit(content=content)
    # todo edit reactions

    extension_controller.update(_poll.jsonify())
    extension_controller.flush()


def get_poll_by_id(bot, guild: discord.Guild, message_id: int):
    extension_controller = bot.get_extension_config_handler(guild, config.EXTENSION_NAME)

    p = None
    for _id, data in extension_controller.get_all().items():
        if data[0] == message_id:
            return poll.Poll.from_dict({_id:data})

def remove_poll(bot, guild: discord.Guild, _poll: poll.Poll):
    extension_controller = bot.get_extension_config_handler(guild, config.EXTENSION_NAME)
    extension_controller.remove(_poll.id)
    extension_controller.flush()

def format_poll(guild: discord.Guild, _poll: poll.Poll) -> str:
    content = "{prefix}{{title}}**\n\n{{poll}}".format(prefix=RP_PREFIX)
    content1 = "{emoji} - {role}{name}\n"

    p = ""
    for r in _poll.param:
        p += content1.format(emoji=r[0], role=guild.get_role(r[2]).mention,
                             name=f"{':' if r[1] else ''} {r[1]}")

    return content.format(title=_poll.title, poll=p)


async def handle_reaction(bot, guild: discord.Guild, channel: discord.TextChannel, message_id, member: discord.Member,
                          emoji) -> discord.Role:
    extension_controller = bot.get_extension_config_handler(guild, config.EXTENSION_NAME)

    for _id, _poll in extension_controller.data.items():
        _message_id = _poll[0]
        _channel_id = _poll[1]

        if message_id == _message_id and channel.id == _channel_id:
            for _role in _poll[3:]:
                if emoji == _role[0]:
                    return guild.get_role(_role[2])


async def add_reaction(bot, guild: discord.Guild, channel: discord.TextChannel, message_id, member: discord.Member,
                          emoji):
    if member.bot:
        return

    role = await handle_reaction(bot, guild, channel, message_id, member, emoji)

    await member.add_roles(role)


async def remove_reaction(bot, guild: discord.Guild, channel: discord.TextChannel, message_id, member: discord.Member,
                          emoji):
    role = await handle_reaction(bot, guild, channel, message_id, member, emoji)

    await member.remove_roles(role)




