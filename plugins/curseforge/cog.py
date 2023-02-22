import discord
from discord.ext import commands
from core import botbase
from core.audio import audiocontroller
from . import config
from core import messages
from core.messages import view_controller
from core import helper
import helper as _helper
from typing import Optional, Tuple, Union, Dict, List
import discord
import cursepy
from discord.ext import tasks
from . import controller
from . import models


class CurseForgeCog(commands.Cog):
    def __init__(self, bot: botbase.BotBase):
        self.bot: botbase.BotBase = bot
        self.logger = _helper.Logger().get_logger(self.__class__.__name__)

        self.logger.info("Starting update routine")
        self.check_updates.start()

    @commands.command(name="cf_create", description="Adds a CurseForge mod to your watchlist")
    async def create_addon(self, ctx):
        extension_controller = self.bot.get_extension_config_handler(ctx.guild, config.EXTENSION_NAME)

        req = "Insert the game ID (e.g. Minecraft -> 432)"
        game_id = await helper.interactive_menu.request_int(self.bot, ctx.channel, ctx.author, req)

        req = "Insert the addon ID (e.g. 'DayOfMind' -> 398186)"
        addon_id = await helper.interactive_menu.request_int(self.bot, ctx.channel, ctx.author, req)

        req = "Do you want a channel for notifications? (yes/no)"
        notify = await helper.interactive_menu.request_bool(self.bot, ctx.channel, ctx.author, req)

        channel = None
        role = None

        if notify:
            req = "Insert the channel for notifications please"
            channel = await helper.interactive_menu.request_channel(self.bot, ctx.channel, ctx.author, req)

            if len(channel) > 0:
                channel = channel[0].id

                req = "Do you want a special role that gets mentioned on each update (default 'everyone')? (yes/no)"
                mention_role = await helper.interactive_menu.request_bool(self.bot, ctx.channel, ctx.author, req)

                if mention_role:
                    req = "Insert the role you want to mention on each update"
                    role = await helper.interactive_menu.request_roles(self.bot, ctx.channel, ctx.author, req)

                    if len(role) > 0:
                        role = role[0].id
            else:
                notify = False

        addon = models.Addon(addon_id, notify, channel, role)
        game_data = extension_controller.get("game")

        if game_data is None:
            game = models.Game(int(game_id), {addon_id: addon})
        else:
            game = models.Game.from_dict(game_data.get(str(game_id)), id=int(game_id))
            game.add_addon(addon)

        all = extension_controller.get("game", {})

        if not str(game_id) in all:
            return

        all.update(game.jsonify())
        extension_controller.update({"game": all})
        extension_controller.flush()

    @commands.command(name="cf_remove", description="Removes a CurseForge mod from the watchlist", )
    async def remove_addon(self, ctx, game_id: int = 0, addon_id: int = 0):
        extension_controller = self.bot.get_extension_config_handler(ctx.guild, config.EXTENSION_NAME)

        if game_id == 0:
            req = "Insert the game ID"
            game_id = await helper.interactive_menu.request_int(self.bot, ctx.channel, ctx.author, req)

        if addon_id == 0:
            req = "Insert the addon ID"
            addon_id = await helper.interactive_menu.request_int(self.bot, ctx.channel, ctx.author, req)

        req = f"Are are about to delete the mod with the id {addon_id} (Game: {game_id}). Are you sure? (yes/no)"
        sure = await helper.interactive_menu.request_bool(self.bot, ctx.channel, ctx.author, req)

        if not sure:
            return

        all = extension_controller.get("game")
        try:
            all[str(game_id)].pop(str(addon_id))
        except KeyError:
            return

        extension_controller.update({"game": all})
        extension_controller.flush()

    @tasks.loop(hours=1)
    async def check_updates(self):
        self.logger.info("performing update")
        await controller.update(self.bot)


async def setup(bot):
    await bot.add_cog(CurseForgeCog(bot))
