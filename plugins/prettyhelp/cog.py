from discord.ext.commands import Cog, Group, Command, HelpCommand, DefaultHelpCommand
from core import botbase
from discord.ext import commands
from typing import Mapping, Optional, List, Dict, Callable, Any
from discord import ui
import discord
import emoji
from core import messages


class PrettyHelp(DefaultHelpCommand):
    def get_command_signature(self, command):
        return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)

    def _add_to_bot(self, bot: commands.Bot) -> None:
        super()._add_to_bot(bot)
        self.bot = bot
        # bot.tree.add_command(self._app_command_callback)

    # def send_cog_help(self, cog: Cog, /) -> None:
    #     print()

    async def send_command_help(self, command: Command, /) -> None:
        # called when ?help command_name
        await self.send_message()

    async def send_error_message(self, error: str, /) -> None:
        # called when ?help command and command not found
        await self.send_message()

    async def send_bot_help(self, mapping: Mapping, /) -> None:
        # called when normal help
        # await self.send_message()

        bot: botbase.BotBase = self.context.bot



    async def send_message(self, title: str = ".", description: str = "."):
        bot: botbase.BotBase = self.context.bot

        footer = f"{bot.command_prefix}help for more info on a command.\nYou can also type {bot.command_prefix}help " \
                 f"<command> for more info about a specific command"
        embed = messages.embeds.build_embed(title=title, description=description, footer=footer)

        await bot.responses.send(channel=self.context.channel, embed=embed, view=HelpView())


class HelpView(ui.View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @ui.button(label="◀", style=discord.ButtonStyle.secondary)
    async def category_left(self, interaction: discord.Interaction, button: ui.Button):
        self.stop()

    @ui.button(label="◁", style=discord.ButtonStyle.secondary)
    async def page_left(self, interaction: discord.Interaction, button: ui.Button):
        self.stop()

    @ui.button(label="▷", style=discord.ButtonStyle.secondary)
    async def page_right(self, interaction: discord.Interaction, button: ui.Button):
        self.stop()

    @ui.button(label="▶", style=discord.ButtonStyle.secondary)
    async def category_right(self, interaction: discord.Interaction, button: ui.Button):
        self.stop()


async def setup(bot: botbase.BotBase):
    bot.help_command = PrettyHelp()
