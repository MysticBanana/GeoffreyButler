import os
from . import FileHandler
from pathlib import Path
import helper
from discord import guild as _guild


class ConfigHandler:
    server_config_name = "server.json"

    def __init__(self, bot, guild: _guild.Guild):
        self.bot = bot

        self.path: Path = Path(os.path.join(os.path.join(bot.project_root, "json"), str(guild.id)))
        self.path.mkdir(parents=True, exist_ok=True)

        self.logger = helper.Logger().get_logger(self.__class__.__name__)
        self.logger.info(f"Loading guild {guild.name} Id: {guild.id}")

        self.config: FileHandler.FileHandler = FileHandler.FileHandler(Path.joinpath(self.path, self.server_config_name))
        self.config.set("id", guild.id)
        self.config.set("name", guild.name)
        self.config.config.auto_save = bot.config.get("FILES", "auto_save", fallback=False)
        self.logger.info(f'Autosave {bot.config.get("FILES", "auto_save", fallback=False)}')




        # you can also modify the server_config file like this
        # self.config["channels"] = {"rule": 1234}




