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

    @commands.command(name="test1", description="test")
    async def test1(self, ctx):
        role_controller = self.bot.get_role_controller(ctx.guild)

        for role in ctx.message.role_mentions:
            role_controller.add_role(role=role)

        self.bot.flush()


async def setup(bot):
    await bot.add_cog(GeoffreyCommands(bot))
