import discord
from discord._types import ClientT
import random
from core import botbase
from discord.ext import commands
from core.utils import interactive_menu as im
# from core.permissions import Permission
from data import models
from core.permissions.decorators import *
from discord.ext import commands, tasks
from discord.ext.commands import Context
from typing import NoReturn
from discord import app_commands
from discord import ui
from core.messages import embeds
import emoji
from typing import Union, Any


from core.permissions import conf
from data import db
from data import db_utils


class RoleSelect(ui.RoleSelect):
    interaction: discord.Interaction = None
    message: discord.Message = None

    def __init__(self, bot, guild: discord.Guild, *args, **kwargs):
        self.bot = bot

        super().__init__(
            placeholder="Select roles",
            min_values=1,
            max_values=3,
            *args,
            **kwargs
        )

    async def callback(self, interaction: discord.Interaction[ClientT]) -> Any:
        self.view.roles = [interaction.guild.get_role(int(i)) for i in interaction.data.get("values", 0)]
        self.view.remove_item(self)
        self.view.add_item(self.view.permission_select)

        await interaction.response.edit_message(view=self.view)


class PermissionSelect(ui.Select):
    interaction: discord.Interaction = None
    message: discord.Message = None

    def __init__(self, bot, guild: discord.Guild, *args, **kwargs):
        self.bot = bot

        options: List[discord.SelectOption] = []

        for op in conf.PermissionType:
            options.append(discord.SelectOption(
                emoji=random.choice(self.bot.emojis),
                # emoji=emoji.emojize(f":regional_indicator_{op.name[0].lower()}:"),
                label=op.name,
            ))

        super().__init__(
            placeholder="Select permissions",
            min_values=1,
            max_values=1,
            options=options,
            *args,
            **kwargs
        )

    async def callback(self, interaction: discord.Interaction[ClientT]) -> Any:
        # await interaction.response.defer()
        self.view.permission = conf.PermissionType[interaction.data.get("values")[0]]
        await self.view.save_selection()
        await interaction.response.send_message("Done", ephemeral=True)


class SetupView(ui.View):
    interaction: discord.Interaction = None
    message: discord.Message = None

    roles: List[discord.Role] = []
    permission: conf.PermissionType = None

    def __init__(self, bot, user: Union[discord.User, discord.Member], guild: discord.Guild, timeout: float = 60.0) -> None:
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.guild = guild

        self.role_select = RoleSelect(self.bot, self.guild)
        self.permission_select = PermissionSelect(self.bot, self.guild)

        self.add_item(self.role_select)

    async def save_selection(self):
        permission = models.Permission(role_ids=[role.id for role in self.roles], level=self.permission.value)
        guild = await db_utils.fetch_guild(guild_id=self.guild.id)
        permissions = models.Permissions.from_dict(guild.permissions)
        permissions.add_permission(permission)

        await db_utils.insert_guild(guild_id=self.guild.id, permissions=permissions.jsonify())

    async def interaction_check(self, interaction: discord.Interaction[discord.Client]) -> bool:
        if interaction.user.id != self.user.id:
            await interaction.response.send_message(
                "You cannot interact with this view.", ephemeral=True
            )
            return False
            # update the interaction attribute when a valid interaction is received
        self.interaction = interaction
        return True

    async def on_timeout(self) -> None:
        # this method is called when the period mentioned in timeout kwarg passes.
        # we can do tasks like disabling buttons here.
        for button in self.children:
            button.disabled = True  # type: ignore
        # and update the message with the update View.
        if self.message:
            await self.message.edit(view=self)

    async def on_error(
            self, interaction: discord.Interaction[discord.Client], error: Exception,
            item: discord.ui.Item[Any]
    ) -> None:
        message = f"An error occurred while processing the interaction for [RolePermissionSetupView]:\n```py\n{error}\n```"
        self.bot._logger.get_logger("Activity").warning(message)
        await interaction.response.send_message(message, ephemeral=True)


class Permissions(commands.Cog):
    def __init__(self, bot: botbase.BotBase):
        self.bot: botbase.BotBase = bot

    @commands.hybrid_command(name="setup_roles", description="Menu to configure roles and permissions on the server")
    @commands.has_permissions(administrator=True)
    async def set_role(self, ctx):

        view = SetupView(self.bot, ctx.author, ctx.guild)

        await self.bot.responses.send(channel=ctx.channel,
                                      view=view,
                                      embed=embeds.build_embed(
                                          author=ctx.author,
                                          title="Role and Permission setup",
                                          description="In this Menu you can configure custom permissions for using this"
                                                      "bot. This means you can give a server role without administrator"
                                                      "permissions on your server, custom permission on the bot."
                                                      "\n\n"
                                                      "Select one or more roles you want to assign custom server "
                                                      "permissions"
                                                      "\n*Note: If you can't see a role"
                                                      "type in the first letters and it will appear*"
                                                      "\n\n"
                                                      "Select the bot permission you want to assign the slected roles."
                                      ))


async def setup(bot):
    await bot.add_cog(Permissions(bot))