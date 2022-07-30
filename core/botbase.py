import discord
from discord.ext import tasks, commands
from pathlib import Path
from data.objects import Guild
from typing import Tuple, List, Dict, Union, Callable, Any
from configparser import ConfigParser
from collections import defaultdict
import helper
import importlib.util
import importlib.machinery
from . import messages


class BotBase(commands.Bot):
    ROOT: Path = ""
    VERSION: str = "1.0"

    GUILDS: Dict[int, Guild] = {}

    conf = "conf.ini"

    responses: messages.MessageController

    @property
    def guilds(self) -> Dict[int, Guild]:
        return BotBase.GUILDS

    @guilds.setter
    def guilds(self, value):
        BotBase.GUILDS = value

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

        self.logger = helper.Logger(path=self.project_root.joinpath("logs"), dev_mode=self.dev_mode).get_logger("Main")
        self.logger.info("Loaded basic setup")

        self.load_guilds_from_config()

        self.logger.info("loading message controller")
        self.responses = messages.MessageController(self)

    def load_guilds_from_config(self):
        """
        Called on start to load all guilds from saved config files
        """

        for file in (self.project_root / "json").iterdir():
            guild_id: int
            try:
                guild_id = int(file.stem)

            except:
                continue

            self.load_guild(Guild.from_guild_id(self, guild_id))

    async def load_plugins(self):
        self.logger.info("Loading Plugins")

        plugin_path = self.project_root.joinpath(self.config.get("FILES", "plugins"))

        if not plugin_path.is_dir():
            return

        # iterate through all modules in the plugins folder
        for module in plugin_path.iterdir():
            await self.load_plugin(plugin_path, module.stem)

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
        self.logger.info(f"Done")

    def register_guild(self, guild: discord.Guild):
        """
        Methode to call when the bot joins or is restarting
         - adding the guild to config if new
         - adding the guild to `GUILDS`
        """

        if guild is None:
            return

        _guild = Guild.from_guild(self, guild)
        self.load_guild(_guild)

    def load_guild(self, guild: Guild):
        self.guilds[guild.guild_id] = guild
        guild.flush()

    def is_guild_registered(self, guild_id: int) -> bool:
        if guild_id in list(self.guilds.keys()):
            return True
        return False

    #  def add_cog(self, cog):
    #     await super(BotBase, self).add_cog(cog)
    #     self.logger.info(f"Cog {cog.qualified_name} loaded")

    async def on_command_error(self, context, exception):
        if context.message:
            await context.message.delete()

        self.logger.warning(exception)

        # Cooldown on command triggered
        if type(exception) == commands.CommandOnCooldown:
            return

        if type(exception) == commands.CommandInvokeError:
            print("i messed up sorry")

    def run(self, **kwargs):
        super().run(self.token, **kwargs)