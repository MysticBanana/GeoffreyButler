from core.messages import view_controller
import discord
from typing import Optional, Tuple, Union, Dict, List, Callable, Any


class RoleSelect(discord.ui.Select):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def callback(self, interaction: discord.Interaction) -> Any:
        print()
