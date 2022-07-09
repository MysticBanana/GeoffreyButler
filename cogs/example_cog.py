import discord
from discord.ext import commands


class GeoffreyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test", description="testing")
    async def test(self, ctx):
        print("hello")

    @commands.command(name="initialise", description="initialise the bot")
    async def initialise(self):
        print("initialising")


def setup(bot):
    bot.add_cog(GeoffreyCommands(bot))
