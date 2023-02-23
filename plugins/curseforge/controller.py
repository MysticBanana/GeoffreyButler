from typing import Optional, Tuple, Union, Dict, List
import discord
from . import config
from data import ConfigLoader
import cursepy
from cursepy.classes import base as cf_base
from . import embeds
from . import models


with open(config.API_KEY_LOCATION, "r") as key_file:
    API_KEY = key_file.read()


async def _notify(bot, guild: discord.Guild, ext_handler, client: cursepy.CurseClient, addon: cf_base.CurseAddon):
    extension_controller: ConfigLoader.ExtensionConfigHandler = ext_handler


async def _update(bot, guild: discord.Guild, ext_handler, client: cursepy.CurseClient, game_id: int, addon_id: int):
    extension_controller: ConfigLoader.ExtensionConfigHandler = ext_handler
    _addon: models.Addon = models.Addon.from_dict(**extension_controller.get("game").get(game_id).get(addon_id))


    game = client.game(game_id)
    addon = client.addon(addon_id)

    e = embeds.info_latest(addon)
    await guild.fetch_roles()

    if _addon.role_id is not None:
        role = guild.get_role(_addon.role_id)
    else:
        role = guild.default_role

    await bot.responses.send(channel_id=_addon.channel_id, content=f"{role.mention}", make_embed=False)
    await bot.responses.send(channel_id=_addon.channel_id, content=f"{role.mention}", embed=e)


async def update(bot):
    # role_controller = self.bot.get_role_controller(ctx.guild)
    for guild_id in bot.guilds.keys():
        guild: discord.Guild = await bot.fetch_guild(guild_id)
        extension_controller: ConfigLoader.ExtensionConfigHandler = bot.get_extension_config_handler(guild, config.EXTENSION_NAME)
        client = cursepy.CurseClient(API_KEY)

        games = extension_controller.get("game", {})

        for game_id, game in games.items():
            addons = game

            for addon_id, addon in addons.items():
                await _update(bot, guild, extension_controller, client, game_id, addon_id)





