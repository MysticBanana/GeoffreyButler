import aiohttp
import discord
from discord.ext import tasks, commands
from pathlib import Path
from data.models import Guild
from typing import Tuple, List, Dict, Union, Callable, Any
from configparser import ConfigParser
import helper
import importlib.util
import importlib.machinery
from . import messages, audio, roles, permissions
import inspect
import traceback
import os
from core.utils.context import Context

import discord.utils

from data import db
from data import db_utils


Bot: "BotBase" = None


initial_extensions = (
    "cogs.events",
    "cogs.general",
    "cogs.permissions",
    "cogs.admin"
)


class BotBase(commands.Bot):
    root: Path = ""
    conf = "conf.ini"
    version = 1.0

    responses: messages.MessageController
    audio_controller: Dict[discord.Guild, audio.Controller] = {}

    bot_app_info: discord.AppInfo

    def __init__(self, command_prefix: str = "?", *args, **kwargs):
        intents = discord.Intents.all()
        super().__init__(command_prefix=command_prefix, intents=intents, **kwargs)

        self.project_root = kwargs.get("root_dir", Path(__file__).parent)

        self.config = ConfigParser()
        self.config.read(self.project_root.joinpath(self.conf))
        self.config.read(self.project_root.joinpath(f"{self.conf}.local"))

        self.token = self.config.get("DEFAULT", "token")
        self.command_prefix = self.config.get("DEFAULT", "prefix", fallback="?")
        self.dev_mode = self.config.getboolean("DEFAULT", "dev_mode", fallback=False)
        self.version = self.config.getfloat("DEFAULT", "version", fallback=self.version)
        self.plugin_path: Path = Path(self.project_root.joinpath(self.config.get("FILES", "plugins")))

        self._logger = helper.Logger(path=self.project_root.joinpath("logs"), dev_mode=self.dev_mode)
        self.logger = self._logger.get_logger("Main")
        self.logger.info("Loaded basic setup")

        db_utils.bot = self

        self.logger.info("loading message controller")
        self.responses = messages.MessageController(self)

        self.logger.info("Reading owners")
        # for owner_id in self.config.get("DISCORD", "owners").split(","):
        #     self.owner_ids.add(owner_id.strip())

        self.logger.info("Done init")

        global Bot
        Bot = self

    async def setup_hook(self) -> None:
        # self.session = aiohttp.ClientSession()

        self.bot_app_info = await self.application_info()
        self.owner_id = self.bot_app_info.owner.id

        self.logger.info("Loading initial Cogs")
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                self.logger.exception('Failed to load extension %s.', extension)

        self.logger.info("Loading extensions")
        extensions = [i.strip() for i in self.config.get("FILES", "extensions").split(",")]
        for extension in extensions:
            try:
                await self.load_extension(f"{self.plugin_path.stem}.{extension}")
            except Exception as e:
                self.logger.exception('Failed to load extension %s.', extension)
        self.logger.info("Done")

    async def get_context(self, origin: Union[discord.Interaction, discord.Message], /, *, cls=Context) -> Context:
        return await super().get_context(origin, cls=cls)

    async def close(self) -> None:
        await super().close()
        # await self.session.close()

    def get_logger(self, name: str):
        return self._logger.get_logger(name)

    def get_audio_controller(self, guild: discord.Guild) -> audio.Controller:
        """Returns an audio controller object for a guild"""

        if guild in self.audio_controller:
            return self.audio_controller.get(guild)

        self.logger.info("loading audio controller")
        controller = audio.Controller(self, guild)
        self.audio_controller[guild] = controller

        return controller

    async def is_guild_registered(self, guild_id: int) -> bool:
        if await db_utils.fetch_guild(guild_id):
            return True
        return False

    async def on_command_error(self, context, exception):
        if context.message:
            await context.message.delete()

        tb = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        message = f"An error occurred while processing the interaction for {str(context.message)}:\n```py\n{tb}\n```"
        self.logger.warning(message)

        # Cooldown on command triggered
        if type(exception) == commands.CommandOnCooldown:
            return

        if type(exception) == commands.CommandInvokeError:
            self.logger.error("Error occurred")

    def run(self, **kwargs):
        super().run(self.token,
                    log_handler=self._logger.file_handler,
                    log_formatter=self._logger.formatter,
                    reconnect=True, **kwargs)
