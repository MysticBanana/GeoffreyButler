import enum
from typing import Optional, Tuple, Union, Dict, List, Callable, Any
from . import colors, embeds, message_config, exceptions
import discord
import discord.ui



class ViewController:
    config: message_config.ViewConfig

    def __init__(self, bot, guild: discord.Guild = None, config: message_config.ViewConfig = message_config.ViewConfig):
        self.bot = bot
        self.guild = guild
        self.config = config

    def get_view(self):
        """
        Returns a view to put into .send(view=...)
        """
        return discord.ui.View()

    def get_select_view(self, callback: Callable):
        pass

    @property
    def view(self):
        return self.get_view()



