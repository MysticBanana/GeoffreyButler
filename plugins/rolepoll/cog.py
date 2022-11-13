import discord
from discord.ext import commands
from core import botbase
from core.audio import audiocontroller
from . import config, util


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
    async def create_poll(self, ctx, category: str, *args):
        role_controller = self.bot.get_role_controller(ctx.guild)

        extension_controller = self.bot.get_extension_config_handler(ctx.guild, config.EXTENSION_NAME)
        if len(args) % 2 != 0:
            return # todo return message

        category = util.Category.from_dict(extension_controller.get(category))

        roles = {}
        for i in range(0, len(args), 2):
            roles[ctx.message.role_mentions[i//2].id] = args[i]

        print()




async def setup(bot):
    await bot.add_cog(RolePollCog(bot))
