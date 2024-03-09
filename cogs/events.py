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

        # todo some message stuff idk

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     """
    #     THIS DOES NOT OVERWRITE THE ON_MESSAGE METHOD
    #
    #     following lines will be executed as well and do not affect the command execution
    #     """
    #
    #     if message.author.bot or not message.guild:
    #         return
    #
    #     guild_id = message.guild.id
    #
    #     if not self.bot.is_guild_registered(guild_id):
    #         self.bot.register_guild(message.guild)


async def setup(bot: botbase.BotBase):
    await bot.add_cog(Events(bot))
