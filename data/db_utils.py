import discord
import asyncio
from data import db
from typing import NoReturn, Union, List, Dict
from sqlalchemy import select, update
from typing import Dict, Any


bot = None


class ServerExtension:
    def __init__(self, bot, extension_name: str):
        self.bot = bot
        self.extension_name = extension_name

    async def set(self, guild_id: int, data: dict):
        guild = await fetch_guild(guild_id)

        extensions = guild.extensions
        extensions.update({
            self.extension_name: data
        })

        await insert_guild(guild_id, extensions=extensions)

    async def fetch(self, guild_id: int, key: str = "") -> Union[Dict, List, str]:
        guild = await fetch_guild(guild_id)

        extension_data = guild.extensions.get(self.extension_name, None)
        if extension_data is None:
            print("Hoho remove me and an extension cant find its data")
            return

        if key:
            return extension_data.get(key)

        return extension_data

    @staticmethod
    async def fast_fetch(extension_name: str, guild_id: int, key: str) -> Union[Dict, List, str]:
        guild = await fetch_guild(guild_id)

        extension_data = guild.extensions.get(extension_name, None)
        if extension_data is None:
            print("Hoho remove me and an extension cant find its data")
            return

        if key:
            return extension_data.get(key)

        return extension_data

class UserServerExtension:
    def __init__(self, bot, extension_name: str, guild_id: int):
        self.bot = bot
        self.extension_name = extension_name
        self.guild_id = guild_id

    async def set(self, user_id: int, data: Union):
        user = await fetch_user(self.guild_id, user_id)

        extensions = user.extensions
        extensions.update({
            self.extension_name: data
        })

        await insert_user(guild_id=self.guild_id, user_id=user_id, extensions=extensions)


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
    Inserts into table by key value (column: value)

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

        if not user:
            user = db.UserServer(discord_id=user_id, server_id=guild_id)
            session.add(user)
            await session.commit()

        return user

async def insert_user(guild_id: int, user_id: int, **kwargs: Dict[str, Any]) -> NoReturn:
    """
    Inserts into table by key value (column: value)

    :param guild_id: Discord guild id
    :param kwargs: inserting values column_name: value
    """

    async with bot.db_session as session:
        result = await session.execute(update(db.UserServer)
                                       .where(db.UserServer.server_id == guild_id
                                              and db.UserServer.discord_id == user_id).values(**kwargs))
        await session.commit()