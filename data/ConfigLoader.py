import os
from . import FileHandler
from pathlib import Path

class ConfigHandler:
    server_config_name = "server.json"

    def __init__(self, bot, server_id: int):
        self.path: Path = Path(os.path.join(os.path.join(bot.project_root, "json"), str(server_id)))
        self.path.mkdir(parents=True, exist_ok=True)

        self.config: FileHandler.FileHandler = FileHandler.FileHandler(Path.joinpath(self.path, self.server_config_name))

        # you can modify the server_config file like this
        # self.config["channels"] = {"rule": 1234}




