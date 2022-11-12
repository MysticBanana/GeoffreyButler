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
        pass

    @property
    def view(self):
        return self.get_view()


class SelectView(discord.ui.Select):

    custom_callback: Callable = None

    def __init__(self, custom_id: str = None, placeholder: str = "", min_value: int = 1, max_values: int = 25,
                 disabled: bool = False, options: List[discord.SelectOption] = None, callback: Callable = None):
        super().__init__(custom_id=custom_id, placeholder=placeholder, min_values=min_value, max_values=max_values,
                         disabled=disabled, options=options)

        self.custom_callback = callback

    async def callback(self, interaction: discord.Interaction) -> Any:
        # execute the given callback before the default one
        if self.custom_callback is not None:
            self.custom_callback(interaction)

        # default callpack





































































































































































