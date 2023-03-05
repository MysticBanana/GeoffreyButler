import discord
from discord.ext import tasks, commands
from pathlib import Path
from data.models import Guild
from typing import Tuple, List, Dict, Union, Callable, Any
from configparser import ConfigParser
import helper
import importlib.util
import importlib.machinery
from . import messages, audio, roles
import inspect


class BotBase(commands.Bot):
    ROOT: Path = ""
    VERSION: str = "1.0"

    GUILDS: Dict[int, Guild] = {}
    PLUGINS: List[str] = []

    conf = "conf.ini"

    responses: messages.MessageController
    audio_controller: Dict[discord.Guild, audio.Controller] = {}

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
        self.VERSION = self.config.getfloat("DEFAULT", "version", fallback=self.VERSION)
        self.plugin_path: Path = Path(self.project_root.joinpath(self.config.get("FILES", "plugins")))

        self.logger = helper.Logger(path=self.project_root.joinpath("logs"), dev_mode=self.dev_mode).get_logger("Main")
        self.logger.info("Loaded basic setup")

        self.load_guilds_from_config()

        self.logger.info("loading message controller")
        self.responses = messages.MessageController(self)

    def load_guilds_from_config(self):
        """
        Called on start to load all guilds from saved config files
        """

        (self.project_root / "json").mkdir(parents=True, exist_ok=True)

        for file in (self.project_root / "json").iterdir():
            guild_id: int
            try:
                guild_id = int(file.stem)

            except:
                continue

            self.load_guild(Guild.from_guild_id(self, guild_id))

    def flush(self):
        for guild_data in self.GUILDS.values():
            guild_data.flush()

    def get_audio_controller(self, guild: discord.Guild) -> audio.Controller:
        """Returns an audio controller object for a guild"""

        if guild in self.audio_controller:
            return self.audio_controller.get(guild)

        self.logger.info("loading audio controller")
        controller = audio.Controller(self, guild)
        self.audio_controller[guild] = controller

        return controller

    def get_role_controller(self, guild: discord.Guild) -> roles.RoleController:
        self.logger.info("loading role controller")
        role_controller = roles.RoleController(self, guild)

        return role_controller

    def get_extension_config_handler(self, guild: discord.Guild, extension_name: str):
        return self.guilds.get(guild.id).register_extension_config_handler(extension_name)

    async def load_plugins(self):
        self.logger.info("Loading Plugins")

        if not self.plugin_path.is_dir():
            return

        # iterate through all modules in the plugins folder
        for module in self.plugin_path.iterdir():
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
        super().run(self.token, **kwargs)
