import discord
from discord.ext import commands
from discord import app_commands


class LevelingCog(commands.Cog, name="Leveling"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", help="Shows info about you")
    async def info(self, ctx, member: discord.Member):
        if member is None:
            member = ctx.author


    




async def setup(bot):
    await bot.add_cog(LevelingCog(bot))
