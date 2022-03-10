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


class Geoffrey(commands.Bot):
    project_root: Path
    conf = "conf.ini"
    VERSION = 1.0

    # all server configloader are saved in it
    SERVERS = dict()

    def __init__(self, command_prefix="?", **kwargs):
        super().__init__(command_prefix, **kwargs)

        self.project_root = kwargs.get("root_dir", Path(__file__).parent)

        self.config = ConfigParser()
        self.config.read(self.project_root.joinpath(self.conf))
        self.config.read(self.project_root.joinpath(f"{self.conf}.local"))

        self.token = self.config.get("DEFAULT", "token")
        self.dev_mode = self.config.getboolean("DEFAULT", "dev_mode", fallback=False)

        self.logger = helper.Logger(path=self.project_root.joinpath("logs"), dev_mode=self.dev_mode).get_logger("Main")

        # setup your commands
        cogs.testcommands.setup(self)

    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        guild_id = message.guild.id
        if guild_id not in list(self.SERVERS.keys()):
            self.SERVERS[guild_id] = data.ConfigHandler(self, guild_id)

        await self.process_commands(message)

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name=f'{self.command_prefix}help || Version: {self.VERSION}'))
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()
        self.logger.info("Successfully loaded")

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