import discord
from discord.ext import commands
from core import botbase
from data import models, db_utils
import data


class Events(commands.Cog):
    def __init__(self, bot: botbase.BotBase):
        self.bot: botbase.BotBase = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.guild.Guild):
        db_utils.register_guild(guild)
        # todo check in settings if welcome message is enabled


async def setup(bot: botbase.BotBase):
    await bot.add_cog(Events(bot))
