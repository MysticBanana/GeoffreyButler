import discord
from discord.ext import commands
from core import botbase
from core.audio import audiocontroller
from . import config, util
from core import messages
from core.messages import view_controller
from core import helper
from typing import Optional, Tuple, Union, Dict, List
from . import models

class RolePollCog(commands.Cog):
    def __init__(self, bot: botbase.BotBase):
        self.bot: botbase.BotBase = bot

    """
    {
        category: "language": {"english": role_id, "german": role_id}
    }
    """

    @commands.command(name="rp_create", description="creates a category with roles")
    async def create_category(self, ctx, category: str, *args):
        role_controller = self.bot.get_role_controller(ctx.guild)
        roles = ctx.message.role_mentions

        if len(roles) > 25:
            return
        # todo error message

        for role in roles:
            role_controller.add_role(role=role)
        self.bot.flush()

        category = util.Category(category, dict.fromkeys([role.id for role in roles]))

        extension_controller = self.bot.get_extension_config_handler(ctx.guild, config.EXTENSION_NAME)
        extension_controller.update(category.jsonify())
        extension_controller.flush()

    @commands.command(name="rp_poll", description="creates a selection menu")
    async def rp_poll(self, ctx):
        # role_controller = self.bot.get_role_controller(ctx.guild)

        extension_controller = self.bot.get_extension_config_handler(ctx.guild, config.EXTENSION_NAME)

        def callback(interaction: discord.Interaction):
            print()

        req = "To create a role poll selection menu type in all possible roles:"
        roles = await helper.interactive_menu.request_roles(self.bot, ctx.channel, ctx.author, req)

        req = "Type in the message displayed above the menu:"
        description = await helper.interactive_menu.request_string(self.bot, ctx.channel, ctx.author, req)

        req = "Type in the text displayed on the selection menu"
        placeholder = await helper.interactive_menu.request_string(self.bot, ctx.channel, ctx.author, req)

        options: List[discord.SelectOption] = []
        for role in roles:
            req = f"Type in the displayed text for role '{role.name}'"
            r = await helper.interactive_menu.request_string(self.bot, ctx.channel, ctx.author, req)
            if len(r) > 100:
                return
            options.append(discord.SelectOption(value=str(role.id), label=r))


        # todo reqest for placeholder

        view = view_controller.ViewController(self.bot, ctx.guild).get_view()
        menu = models.RoleSelect(min_values=1, max_values=25, placeholder=placeholder, options=options)
        view.add_item(menu)

        await self.bot.responses.send(view=view, channel=ctx.channel, make_embed=False, content=description)

        return
        # send role stuff here
        # todo not hardcoded
        options = [discord.SelectOption(label=roles[role_id], value=role_id, default=False) for role_id in roles]
        sel_view = discord.ui.Select(custom_id="rolepoll", placeholder="Select your roles", options=options)

        vc = view_controller.ViewController(self.bot, ctx.guild)
        view = vc.get_view()
        view.add_item(sel_view)

        await self.bot.responses.send(view=view, channel=ctx.channel, make_embed=False, content="")



async def setup(bot):
    await bot.add_cog(RolePollCog(bot))
