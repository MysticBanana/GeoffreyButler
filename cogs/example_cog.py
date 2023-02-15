import discord
from discord.ext import commands
from core import botbase
from core import helper

import discord
from discord.ext import commands
from core import botbase
from core.audio import audiocontroller

from core import messages
from core.messages import view_controller
from core import helper
from typing import Optional, Tuple, Union, Dict, List
from plugins.rolepoll import models


class GeoffreyCommands(commands.Cog):
    def __init__(self, bot: botbase.BotBase):
        self.bot: botbase.BotBase = bot

    @commands.command(name="test", description="testing")
    async def test(self, ctx):
        await self.bot.responses.send(ctx.channel, content="test", title="test")

    @commands.command(name="initialise", description="initialise the bot")
    async def initialise(self, ctx):
        print("initialising")

    @commands.command(name="test1", description="test")
    async def test1(self, ctx):
        pass
        # view = DropdownView()
        # await ctx.send("pick what ever", view=view)
        #
        # await self.bot.responses.send(view=view, channel=ctx.channel, make_embed=False, content="description")

    @commands.command(name="imenu", description="testing interactive menu")
    async def imenu(self, ctx):
        m = helper.interactive_menu.Menu(self.bot, channel=ctx.channel, user=ctx.author, options=["1?", "Is this a test?"])
        result = await m.get_input()

        print(result)


async def setup(bot):
    await bot.add_cog(GeoffreyCommands(bot))
