import discord
from discord.ext import commands


class SampleExt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sample-ext", description="sample-ext")
    async def sample(self, ctx):
        print("sample-ext")


def setup(bot):
    bot.add_cog(SampleExt(bot))
