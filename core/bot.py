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


class Geoffrey(botbase.BotBase):
    def __init__(self, command_prefix="?", **kwargs):
        super().__init__(command_prefix, **kwargs)

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name=f'{self.command_prefix}help || Version: {self.VERSION}'))
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()
        self.logger.info("Successfully loaded")
        self.logger.info(f"Online | prefix:{self.command_prefix}")

        self.logger.info("Loading Plugins")
        await self.load_plugins()
        self.logger.info("Plugins loaded")

        self.logger.info("setting up cogs")
        # setup your commands
        await cogs.example_cog.setup(self)
        await cogs.events.setup(self)

        print("ready")


