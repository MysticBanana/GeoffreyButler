from typing import Optional, Tuple, Union, Dict, List
import discord
from core import messages
from cursepy.classes import base as cf_base


def info(addon: cf_base.CurseAddon) -> discord.Embed:

    fields = []

    embed = messages.embeds.build_embed(
        title=f"**{addon.name}**",
        description=f"{addon.summary}",
        thumbnail=addon.raw["data"]["logo"]["thumbnailUrl"],
        fields=fields,

    )
    return embed
