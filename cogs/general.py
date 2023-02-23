import discord
from discord.ext import commands
from core import botbase
from core import helper
from typing import Optional, Tuple, Union, Dict, List
from core import messages


class General(commands.Cog):
    def __init__(self, bot: botbase.BotBase):
        self.bot: botbase.BotBase = bot

    @commands.command(name="about", description="Shows information about the bot")
    async def about(self, ctx):
        about = """I am a multipurpose and modular discord bot created by MysticBanana"""

        embed = messages.embeds.build_embed(
            title="About",
            description=about,
            fields=[
                {"name": "Links", "value": "[Github](https://github.com/MysticBanana/GeoffreyButler)", "inline": False}
            ]
        )

        await self.bot.responses.send(embed=embed, channel=ctx.channel)

    @commands.command(name="announce", description="Create an announcement for you")
    async def announce(self, ctx):

        req = "Insert the title"
        title = await helper.interactive_menu.request_string(self.bot, ctx.channel, ctx.author, req)

        req = "Insert the link to the displayed thumbnail ('.' for None)"
        thumbnail = await helper.interactive_menu.request_string(self.bot, ctx.channel, ctx.author, req)
        if thumbnail == ".":
            thumbnail = None

        req = "Insert the description of your announcement"
        description = await helper.interactive_menu.request_string(self.bot, ctx.channel, ctx.author, req)

        req = "Do you want to mention roles?"
        mention = await helper.interactive_menu.request_bool(self.bot, ctx.channel, ctx.author, req)

        roles = []
        if mention:
            req = "Insert the roles you want to mention"
            roles = await helper.interactive_menu.request_roles(self.bot, ctx.channel, ctx.author, req)

        req = "Insert the channel you want your message to be posted"
        channel = await helper.interactive_menu.request_channel(self.bot, ctx.channel, ctx.author, req)

        embed = messages.embeds.build_embed(
            title=title,
            description=description,
            thumbnail=thumbnail
        )

        if len(roles) > 0:
            await self.bot.responses.send(channel=channel[0], content=" ".join([i.mention for i in roles]), make_embed=False)

        await self.bot.responses.send(channel=channel[0], embed=embed)

    @commands.command(name="edit_announcement", description="Edits a already created message by the bot")
    async def about(self, ctx):
        pass

async def setup(bot):
    await bot.add_cog(General(bot))
