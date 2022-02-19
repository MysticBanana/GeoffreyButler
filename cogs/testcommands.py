import discord
from discord.ext import commands

class GeoffreyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        pass

    @commands.command(name="test", description="testing")
    async def test(self, ctx):
        pass

    # TODO: rpg

def setup(bot):
    bot.add_cog(GeoffreyCommands(bot))