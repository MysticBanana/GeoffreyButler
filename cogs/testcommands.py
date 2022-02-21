import discord
from discord.ext import commands
import rolePlayGame as rpg

class GeoffreyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        pass

    @commands.command(name="test", description="testing")
    async def test(self, ctx):
        pass

    @commands.command(name="rpgStart", description="starting a RPG text-message-like adventure in DM")
    async def rpgStart(self, user):
        rolePlay=rpg.RPG()
        rolePlay.start(user, user)

    @commands.command(name="initialise", description="initialise the bot")
    async def initialise(self):
        print("initialising")

    # TODO: rolePlayGame


def setup(bot):
    bot.add_cog(GeoffreyCommands(bot))
