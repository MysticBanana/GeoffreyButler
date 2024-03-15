from typing import Tuple, List, Dict, Union, Callable, Any, Optional
import discord
from . import config
from .models import poll
from data import db, db_utils
from discord.ext.commands import Context
from discord.utils import get


RP_PREFIX = "**RolePoll - "


async def simple_poll(bot, guild: discord.Guild, channel: discord.TextChannel, p: poll.Poll):
    content = f"**{p.title}**\n\n"

    for option in p.param:
        _emoji, description = option

        content += f"{_emoji} - {description}\n"

    await bot.responses.send(channel=channel, make_embed=False, content=content, reactions=p.emojis)


async def title_poll(bot, guild: discord.Guild, channel: discord.TextChannel, p: poll.Poll):
    await bot.responses.send(channel=channel, make_embed=False, content=f"{p.title}", reactions=p.emojis)


async def create_poll(bot, guild: discord.Guild, channel: discord.TextChannel, _poll: poll.Poll):
    content = format_poll(guild, _poll)
    msg: discord.Message = await bot.responses.send(channel=channel, make_embed=False, content=content, reactions=_poll.emojis)
    _poll.message_id = msg.id


async def modify_poll(bot, guild: discord.Guild, ctx: discord.ext.commands.Context, reference: discord.MessageReference,
                      _poll: poll.Poll):
    content = format_poll(guild, _poll)

    message = await ctx.fetch_message(reference.message_id)
    await message.edit(content=content)

    for reaction in _poll.emojis:
        await message.add_reaction(reaction)

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


def poll_from_reference(reference: discord.MessageReference = None, message: discord.Message = None) -> poll.Poll:
    content = reference.resolved.content if reference is not None else message.content
    role_mentions = reference.resolved.role_mentions if reference is not None else message.role_mentions

    title = content.split(RP_PREFIX)[1].split("**")[0]

    content = content.split("\n", 2)[2]
    roles: List[int] = [i.id for i in role_mentions]

    emojis = []
    description = []

    for line in content.split("\n"):
        e, d = line.split(" - ")
        d = d.rsplit(":", 1)[1]

        emojis.append(e)
        description.append(d)

    options = []
    for i in range(len(roles)):
        options.append([emojis[i], description[i], roles[i]])

    return poll.Poll(title, options)


async def handle_reaction_message(message: discord.Message, emoji) -> discord.Role:
    _poll = poll_from_reference(message=message)
    return _poll.get_role_by_emoji(emoji)


async def add_reaction(guild: discord.Guild, message: discord.Message, member: discord.Member, emoji):
    if member.bot:
        return

    role_id = await handle_reaction_message(message, emoji)
    role = get(guild.roles, id=role_id)
    await member.add_roles(role)


async def remove_reaction(guild: discord.Guild, message: discord.Message, member: discord.Member, emoji):
    if member.bot:
        return

    role_id = await handle_reaction_message(message, emoji)
    role = get(guild.roles, id=role_id)
    await member.remove_roles(role)




