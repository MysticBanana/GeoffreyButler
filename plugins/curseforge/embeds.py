from typing import Optional, Tuple, Union, Dict, List
import discord
from core import messages
from cursepy.classes import base as cf_base

nl = "\n"


def info_latest(addon: cf_base.CurseAddon) -> discord.Embed:

    fileId = addon.raw["data"]["latestFiles"][-1]["serverPackFileId"]
    download_url = f'{addon.url}/download/{addon.raw["data"]["latestFiles"][-1]["id"]}'

    links = ' | '.join([
        f'[Download]({download_url})',
        f"[Changelog]({addon.raw['data']['links']['websiteUrl']}/{fileId})",
        f"[Website]({addon.raw['data']['links']['websiteUrl']})"
        ])

    fields = [
        {"name": f"Latest version", "value": f"{addon.raw['data']['latestFiles'][-1]['displayName']}", "inline": True},
        {"name": "Categories", "value": f"{'; '.join([i.name for i in addon.all_categories])}", "inline": True},
        {"name": "Authors", "value": f"{nl.join([f'• {i.name}' for i in addon.authors])}", "inline": False},
        {"name": "Links", "value": f"{links}", "inline": False}
    ]

    embed = messages.embeds.build_embed(
        title=f"**{addon.name}**",
        description=f"{addon.summary}",
        thumbnail=addon.raw["data"]["logo"]["thumbnailUrl"],
        fields=fields,

    )
    return embed
