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


class Geoffrey(commands.Bot):
    project_root: Path
    conf = "conf.ini"
    VERSION = 1.0

    # all server configloader are saved in it
    SERVERS = dict()

    # where all plugins getting stored (python packages)
    PLUGINS = []

    def __init__(self, command_prefix="?", **kwargs):
        super().__init__(command_prefix, **kwargs)

        self.project_root = kwargs.get("root_dir", Path(__file__).parent)

        self.config = ConfigParser()

        self.config.read(self.project_root.joinpath(self.conf))
        self.config.read(self.project_root.joinpath(f"{self.conf}.local"))

        self.token = self.config.get("DEFAULT", "token")
        self.command_prefix = self.config.get("DEFAULT", "prefix", fallback="?")
        self.dev_mode = self.config.getboolean("DEFAULT", "dev_mode", fallback=False)

        self.logger = helper.Logger(path=self.project_root.joinpath("logs"), dev_mode=self.dev_mode).get_logger("Main")
        self.logger.info("Loaded basic setup")

        if not self.project_root.joinpath(f"{self.conf}.local").is_file():
            self.logger.critical("local config is not created!")

        # setup your commands
        cogs.example_cog.setup(self)

    async def load_plugins(self):
        plugin_path = self.project_root.joinpath(self.config.get("FILES", "plugins"))

        if not plugin_path.is_dir():
            return

        # iterate through all modules in the plugins folder
        for module in plugin_path.iterdir():
            await self.load_plugin(plugin_path, module.stem)

    async def load_plugin(self, plugin_path, name: str):
        loader_details: Tuple = (
            importlib.machinery.SourceFileLoader,
            importlib.machinery.SOURCE_SUFFIXES
        )

        plugin_finder = importlib.machinery.FileFinder(str(plugin_path), loader_details)
        spec = plugin_finder.find_spec(name)

        self._load_from_module_spec(spec, name)

    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        guild_id = message.guild.id
        if guild_id not in list(self.SERVERS.keys()):
            self.SERVERS[guild_id] = data.ConfigHandler(self, message.guild)

        await self.process_commands(message)

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name=f'{self.command_prefix}help || Version: {self.VERSION}'))
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()
        self.logger.info("Successfully loaded")
        self.logger.info(f"Online | prefix:{self.command_prefix}")

        self.logger.info("Loading Plugins")
        await self.load_plugins()
        self.logger.info("Plugins loaded")

        print("ready")

    def add_cog(self, cog):
        super(Geoffrey, self).add_cog(cog)
        self.logger.info(f"Cog {cog.qualified_name} loaded")

    async def on_command_error(self, context, exception):
        if context.message:
            await context.message.delete()

        self.logger.error(exception)

        # Cooldown on command triggered
        if type(exception) == commands.CommandOnCooldown:
            pass

        if type(exception) == commands.CommandInvokeError:
            print("i messed up sorry")

    def run(self):
        super().run(self.token)


if __name__ == "__main__":
    bot = Geoffrey()
    bot.run()