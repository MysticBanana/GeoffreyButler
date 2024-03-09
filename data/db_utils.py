import discord
import asyncio
from data import db
from typing import NoReturn
from sqlalchemy import select, update
from typing import Dict, Any


bot = None


class ServerExtensions:
    def __init__(self, bot, extension_name: str):
        self.bot = bot
        self.extension_name = extension_name

    async def add(self, guild_id: int, data: dict):
        guild = await fetch_guild(guild_id)

        extensions = guild.extensions
        extensions.update({
            self.extension_name: data
        })

        await insert_guild(guild_id, extensions=extensions)


async def register_guild(guild: discord.Guild) -> NoReturn:
    async with bot.db_session as session:
        server = db.Server(server_id=guild.id,
                           server_name=guild.name)

        session.add(server)
        await session.commit()


async def fetch_guild(guild_id: int) -> db.Server:
    async with bot.db_session as session:
        guild = await session.get(db.Server, guild_id)
        return guild


async def insert_guild(guild_id: int, **kwargs: Dict[str, Any]) -> NoReturn:
    """
    Insers into table by key value (column: value)

    :param guild_id: Discord guild id
    :param kwargs: inserting values column_name: value
    """

    async with bot.db_session as session:
        result = await session.execute(update(db.Server).where(db.Server.server_id == guild_id).values(**kwargs))
        await session.commit()


async def fetch_guilds():
    async with bot.db_session as session:
        result = await session.execute(select(db.Server))
        # frozen = result.freeze()
        return result.scalars().all()


async def fetch_global_user(user_id: int) -> db.User:
    async with bot.db_session as session:
        user = await session.get(db.User, user_id)
        return user


async def fetch_user(guild_id: int, user_id: int) -> db.UserServer:
    async with bot.db_session as session:
        # user = await session.get(db.UserServer, {"discord_id": user_id,
        #                                          "server_id": guild_id})
        user = await session.get(db.UserServer, (user_id, guild_id))
        return user
