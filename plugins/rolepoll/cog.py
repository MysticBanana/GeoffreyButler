import discord
from discord.ext import commands
from core import botbase
from core.audio import audiocontroller


class RolePollCog(commands.Cog):
    def __init__(self, bot: botbase.BotBase):
        self.bot: botbase.BotBase = bot

    # @commands.command(name="showroles", help="shows all roles linked to a category")
    # def show_roles(self, ctx, category: str = ""):
    #     pass
    #
    # @commands.command(name="createcategory", help="creates a category to add roles to")
    # def create_category(self, ctx, category: str = ""):
    #     pass


async def setup(bot):
    await bot.add_cog(RolePollCog(bot))
