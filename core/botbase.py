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

import discord.utils

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from data import db
from data import db_utils


class BotBase(commands.Bot):
    ROOT: Path = ""
    VERSION: str = "1.0"
    PLUGINS: List[str] = []

    conf = "conf.ini"

    responses: messages.MessageController
    audio_controller: Dict[discord.Guild, audio.Controller] = {}

    @property
    def project_root(self) -> Path:
        return BotBase.ROOT

    @project_root.setter
    def project_root(self, value):
        BotBase.ROOT = value

    def __init__(self, command_prefix: str = "?", *args, **kwargs):
        intents = discord.Intents.all()
        super().__init__(command_prefix, intents=intents, *args, **kwargs)

        self.project_root = kwargs.get("root_dir", Path(__file__).parent)

        self.config = ConfigParser()

        self.config.read(self.project_root.joinpath(self.conf))
        self.config.read(self.project_root.joinpath(f"{self.conf}.local"))

        self.token = self.config.get("DEFAULT", "token")
        self.command_prefix = self.config.get("DEFAULT", "prefix", fallback="?")
        self.dev_mode = self.config.getboolean("DEFAULT", "dev_mode", fallback=False)
        self.VERSION = self.config.getfloat("DEFAULT", "version", fallback=self.VERSION)
        self.plugin_path: Path = Path(self.project_root.joinpath(self.config.get("FILES", "plugins")))

        self._logger = helper.Logger(path=self.project_root.joinpath("logs"), dev_mode=self.dev_mode)
        self.logger = self._logger.get_logger("Main")
        self.logger.info("Loaded basic setup")

        db_utils.bot = self

        self.logger.info("loading message controller")
        self.responses = messages.MessageController(self)

        self.logger.info("Reading owners")
        for owner_id in self.config.get("DISCORD", "owners").split(","):
            self.owner_ids.add(owner_id.strip())

        self.logger.info("Done init")

    def get_audio_controller(self, guild: discord.Guild) -> audio.Controller:
        """Returns an audio controller object for a guild"""

        if guild in self.audio_controller:
            return self.audio_controller.get(guild)

        self.logger.info("loading audio controller")
        controller = audio.Controller(self, guild)
        self.audio_controller[guild] = controller

        return controller

    async def load_plugins(self):
        self.logger.info("Loading Plugins")

        if not self.plugin_path.is_dir():
            return

        extensions = [i.strip() for i in self.config.get("FILES", "extensions").split(",")]

        # iterate through all modules in the plugins folder
        for module in self.plugin_path.iterdir():
            if module.name in extensions:
                await self.load_plugin(self.plugin_path, module.stem)

        self.logger.info("Successfully loaded all plugins")

    async def load_plugin(self, path: Path, name: str):
        self.logger.info(f"Loading plugin `{name}` from path `{path}`")

        loader_details: Tuple = (
            importlib.machinery.SourceFileLoader,
            importlib.machinery.SOURCE_SUFFIXES
        )

        plugin_finder = importlib.machinery.FileFinder(str(path), loader_details)
        spec = plugin_finder.find_spec(name)

        await self._load_from_module_spec(spec, name)
        self.PLUGINS.append(name)

        self.logger.info(f"Done")

    async def unload_plugin(self, name: str):
        await self.unload_extension(name)
        self.PLUGINS.remove(name)

    async def reload_plugin(self, name: str):
        await self.unload_plugin(name)
        await self.load_plugin(self.plugin_path, name)

    async def is_guild_registered(self, guild_id: int) -> bool:
        if await db_utils.fetch_guild(guild_id):
            return True
        return False

    async def on_command_error(self, context, exception):
        if context.message:
            await context.message.delete()

        self.logger.warning(exception)

        # Cooldown on command triggered
        if type(exception) == commands.CommandOnCooldown:
            return

        if type(exception) == commands.CommandInvokeError:
            print("i messed up sorry")

    async def setup_hook(self) -> None:
        for name, view in inspect.getmembers(messages.views):
            try:
                self.add_view(view)
            except TypeError:
                pass

    def run(self, **kwargs):
        super().run(self.token,
                    log_handler=self._logger.file_handler,
                    log_formatter=self._logger.formatter,
                    reconnect=True, **kwargs)
