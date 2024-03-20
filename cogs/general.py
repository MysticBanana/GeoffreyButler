import random

import discord
from discord.ext import commands
from core import botbase
from core import utils
from typing import Optional, Tuple, Union, Dict, List
from core import messages
from data import db, db_utils
from discord.ext.commands import Context
from discord import app_commands


class General(commands.Cog, name="General"):
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
        # await ctx.message.delete()

    @commands.command(name="roll", description="Returns a random number")
    async def roll(self, ctx, number: int = 6):
        if number > 100:
            await self.bot.responses.send(channel=ctx.channel, content="This number is too high (max 100).")
            return

        embed = messages.embeds.build_embed(
            title=f"**Random number**",
            description=f"{random.randint(1, number)}"
        )

        await self.bot.responses.send(channel=ctx.channel, embed=embed)
        await ctx.message.delete()

    @commands.command(name="purge", description="Deletes an amount of messages")
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, number: int = 1):
        if number > 100:
            await self.bot.responses.send(channel=ctx.channel, content="This number is too high (max 100).")
            return

        await ctx.channel.purge(limit=number)

    @commands.command(name="announce", description="Create an announcement for you")
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx):

        req = "Insert the title"
        title = await utils.interactive_menu.request_string(self.bot, ctx.channel, ctx.author, req)

        req = "Insert the link to the displayed thumbnail"
        thumbnail = await utils.interactive_menu.request_url(self.bot, ctx.channel, ctx.author, req)
        if thumbnail == "":
            thumbnail = None

        req = "Insert the description of your announcement"
        description = await utils.interactive_menu.request_string(self.bot, ctx.channel, ctx.author, req)

        req = "Do you want to mention roles? (Yes / No)"
        mention = await utils.interactive_menu.request_bool(self.bot, ctx.channel, ctx.author, req)

        roles = []
        if mention:
            req = "Insert the roles you want to mention"
            roles = await utils.interactive_menu.request_roles(self.bot, ctx.channel, ctx.author, req)

        req = "Insert the channel(s) you want your message to be posted"
        channels = await utils.interactive_menu.request_channel(self.bot, ctx.channel, ctx.author, req)

        embed = messages.embeds.build_embed(
            title=f"**{title}**",
            description=description,
            thumbnail=thumbnail
        )

        for c in channels:
            if len(roles) > 0:
                await self.bot.responses.send(channel=c, content=" ".join([i.mention for i in roles]), make_embed=False)

            await self.bot.responses.send(channel=c, embed=embed)

        await ctx.message.delete()

    @commands.command(name="edit_announcement", description="Edits a already created message by the bot")
    @commands.has_permissions(administrator=True)
    async def edit_announcement(self, ctx):
        req = "Enter the message id"
        message_id = await utils.interactive_menu.request_string(self.bot, ctx.channel, ctx.author, req)

        # this might not work with messages in different channels
        message = await ctx.fetch_message(message_id)

        req = "Insert the title"
        title = await utils.interactive_menu.request_string(self.bot, ctx.channel, ctx.author, req)

        req = "Insert the link to the displayed thumbnail"
        thumbnail = await utils.interactive_menu.request_string(self.bot, ctx.channel, ctx.author, req)

        req = "Insert the description of your announcement"
        description = await utils.interactive_menu.request_string(self.bot, ctx.channel, ctx.author, req)

        embed = messages.embeds.build_embed(
            title=f"**{title}**",
            description=description,
            thumbnail=thumbnail
        )

        await message.edit(embed=embed)
        await ctx.message.delete()

    # @commands.hybrid_command(name="echo", description="test", with_app_command=True)
    # # @app_commands.describe(message="The message to echo")
    # # @commands.has_permissions(administrator=True)
    # async def echo(self, ctx: Context, message: str = ""):
    #
    #     # await db_utils.register_guild(ctx.guild)
    #     # data: db.Server = await db_utils.fetch_guild(ctx.guild.id)
    #     # print(data.server_name)
    #     #
    #     # data: List[db.Server] = await db_utils.fetch_guilds()
    #     await ctx.send("test", reference=ctx.message)
    #     await ctx.message.delete()
    #
    # @echo.autocomplete("message")
    # async def echo_autocomplete(self,
    #                         interaction: discord.Interaction,
    #                         current: str,
    #                         ) -> List[app_commands.Choice[str]]:
    #     return [app_commands.Choice(name="Test", value="test")]

    # @commands.command(name="sync", description="Admin only - syncs commands")
    # @commands.has_permissions(administrator=True)
    # # @commands.is_owner()
    # async def sync(self, ctx: Context):
    #     self.bot.logger.warning("Syncing slash commands")
    #     await self.bot.tree.sync(guild=ctx.guild)
    #
    #     # await self.bot.tree.sync()
    #     await ctx.send('Command tree synced.')

    @commands.command(name="register", description="register")
    @commands.has_permissions(administrator=True)
    async def register(self, ctx: Context):
        await db_utils.register_guild(ctx.guild)
        await ctx.message.delete()

    # @commands.command(name="sync", description="syncs slash commands")
    # @commands.is_owner()
    # async def sync(self, ctx):
    #     # print("sync command")
    #     # if ctx.author.id == OWNER_USERID:
    #     await self.bot.tree.sync()
    #     await ctx.send('Command tree synced.')


async def setup(bot):
    await bot.add_cog(General(bot))
