from core.messages import view_controller
import discord
from typing import Optional, Tuple, Union, Dict, List, Callable, Any


class RoleSelect(view_controller.SelectView):
    async def callback(self, interaction: discord.Interaction) -> Any:
        await super(RoleSelect, self).callback(interaction)


