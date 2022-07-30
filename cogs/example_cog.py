import discord
from discord.ext import commands
from core import botbase


class GeoffreyCommands(commands.Cog):
    def __init__(self, bot: botbase.BotBase):
        self.bot: botbase.BotBase = bot

    @commands.command(name="test", description="testing")
    async def test(self, ctx):
        await self.bot.responses.send(ctx.channel, content="test", title="test")

    @commands.command(name="initialise", description="initialise the bot")
    async def initialise(self, ctx):
        print("initialising")


async def setup(bot):
    await bot.add_cog(GeoffreyCommands(bot))
