import discord
import os
import cogs
from discord.ext import tasks, commands
from pathlib import Path
import datetime
import data


class Geoffrey(commands.Bot):
    project_root = Path(__file__).parent.parent
    VERSION = 1.0

    # all server configloader are saved in it
    SERVERS = dict()

    def __init__(self, command_prefix="?", **options):
        super().__init__(command_prefix, **options)

        cogs.testcommands.setup(self)

        with open(os.path.join(self.project_root, "TOKEN.txt"), "r") as token_file:
            self.token = token_file.read().strip()

        # todo create proper logging


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

    async def on_command_error(self, context, exception):
        if context.message:
            await context.message.delete()

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