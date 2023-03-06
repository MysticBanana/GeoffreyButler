from discord.ext import commands
from core import botbase


class GeoffreyCommands(commands.Cog):
    def __init__(self, bot: botbase.BotBase):
        self.bot: botbase.BotBase = bot

    @commands.command(name="test", description="example")
    async def test(self, ctx):
        await self.bot.responses.send(ctx.channel, content="test", title="title8")


async def setup(bot):
    await bot.add_cog(GeoffreyCommands(bot))
