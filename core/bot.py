import discord
import os
import cogs
from discord.ext import tasks, commands
from pathlib import Path
import datetime
import data
from configparser import ConfigParser
import helper
import logging
import importlib.util
import importlib.machinery
from typing import Tuple, List, Union, Callable
import inspect
from core import botbase
from . import messages
from pretty_help import PrettyHelp
from core.messages import message_config

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from  sqlalchemy.dialects.sqlite import aiosqlite
from data import db
from discord import app_commands


class Geoffrey(botbase.BotBase):

    instance: "Geoffrey"

    def __init__(self, command_prefix="?", **kwargs):
        super().__init__(command_prefix, **kwargs)

        self.color_theme = message_config.ThemeBlue
        Geoffrey.instance = self
        self.help_command = PrettyHelp(color=message_config.get_color(self.color_theme.DARK.value),
                                       delete_invoke=True,
                                       ending_note=f"Type {self.command_prefix}help command for more info on a command."
                                                   f"\nDiscord bot by MysticBanana",
                                       )

        # self._tree = app_commands.CommandTree(self)

    @property
    def db_session(self) -> AsyncSession:
        return self.session()

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name=f'{self.command_prefix}help || Version: {self.VERSION}'))
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()
        self.logger.info("Successfully loaded")
        self.logger.info(f"Online | prefix:{self.command_prefix}")



    async def setup_hook(self) -> None:

        self.logger.info("Setting up database")
        engine = create_async_engine(
            "sqlite+aiosqlite:///sqlite.db",
            # echo=True,
        )

        # async with engine.begin() as conn:
        #     await conn.run_sync(db.Base.metadata.drop_all)
        #     await conn.run_sync(db.Base.metadata.create_all)

        # expire_on_commit=False will prevent attributes from being expired
        # after commit.
        self.session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        self.logger.info("Done")

        self.logger.info("Loading Plugins")
        await self.load_plugins()
        self.logger.info("Done")

        self.logger.info("Setting up Cog default modules")
        # setup your commands
        await cogs.example_cog.setup(self)
        await cogs.events.setup(self)
        await cogs.general.setup(self)
        await cogs.permissions.setup(self)
        self.logger.info("Done")

        for name, view in inspect.getmembers(messages.views):
            try:
                self.add_view(view)
            except TypeError:
                pass
