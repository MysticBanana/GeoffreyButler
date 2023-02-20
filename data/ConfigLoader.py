import os
from . import FileHandler
from pathlib import Path
import helper
from typing import Dict, Any


class ConfigHandler:
    server_config_name = "server.json"
    _exists = False

    extension_handler: Dict[str, "ExtensionConfigHandler"] = {}

    def __init__(self, bot, guild):
        self.bot = bot
        self.guild = guild
        self.extension_handler = {}

        self.path: Path = bot.project_root / "json" / str(guild.guild_id)
        self.path.mkdir(parents=True, exist_ok=True)

        self.logger = helper.Logger().get_logger(self.__class__.__name__)

        if (self.path / self.server_config_name).is_file():
            self._exists = True

        self.config: FileHandler.FileHandler = FileHandler.FileHandler(
            Path.joinpath(self.path, self.server_config_name))

        self.logger.info(f"Loading guild {guild.name} Id: {guild.guild_id}")

        self.config.update(guild.jsonify())

        self.config.config.auto_save = bot.config.get("FILES", "auto_save", fallback=False)
        self.logger.info(f'Autosave {bot.config.get("FILES", "auto_save", fallback=False)}')

    def flush(self):
        self.config.update(self.guild.jsonify())
        self.config.flush()

    def exists(self) -> bool:
        return self._exists

    @staticmethod
    def guild_data_from_id(bot, guild_id: int):
        path: Path = bot.project_root / "json" / str(guild_id)

        if not (path / ConfigHandler.server_config_name).is_file():
            return

        config: FileHandler.FileHandler = FileHandler.FileHandler(
            Path.joinpath(path, ConfigHandler.server_config_name))

        return config.content


class ExtensionConfigHandler:

    config_handler: ConfigHandler
    extension_name: str
    data: dict

    def __init__(self, config_handler: ConfigHandler, extension_name):
        self.config_handler = config_handler
        self.extension_name = extension_name
        self.data = self.config_handler.config.content.get("extension", {}).get(self.extension_name) or {}

    def update(self, data: Dict):
        self.data.update(data)

    def get(self, name: str) -> dict:
        return self.data.get(name, {})

    def remove(self, key: Any) -> None:
        self.data.pop(key)

    def flush(self):
        self.config_handler.guild.set_extension_data(self.extension_name, self.data)
        self.config_handler.flush()


