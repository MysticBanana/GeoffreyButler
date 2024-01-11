import random
from typing import Optional, Tuple, Union, Dict, List, Any
import discord
from discord import ui
import emoji
import validators


class Menu:

    """
    Used to get multiple user inputs
    """

    def __init__(self, bot, channel, user: discord.Member, options: List[str]):
        """
        :param bot: bot object
        :param options: list of questions to ask
        """

        self.bot = bot
        self.channel = channel
        self.user = user
        self.options = options

    async def get_input(self) -> List[Any]:

        # user input
        responses = []

        for req in self.options:
            await self.bot.responses.send(channel=self.channel, make_embed=False, content=req)

            msg = await self.bot.wait_for("message", check=lambda m: (m.author == self.user and m.channel == self.channel), timeout=30.0)
            responses.append(msg.role_mentions or msg.content)

        return responses

    async def get_raw_input(self) -> List[str]:

        # user input
        responses = []

        for req in self.options:
            await self.bot.responses.send(channel=self.channel, make_embed=False, content=req)

            msg = await self.bot.wait_for("message", check=lambda m: (m.author == self.user and m.channel == self.channel), timeout=30.0)
            responses.append(msg.content)

        return responses


class UiMenu(ui.Modal):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        options: Tuple[Union[Dict, discord.ui.TextInput]] = kwargs.get("options", tuple())

        for option in options:
            if isinstance(options, discord.ui.TextInput):
                self.add_item(option)
                continue

            self.add_item(discord.ui.TextInput(**option))

    async def on_submit(self, interaction: discord.Interaction) -> None:
        pass  # await interaction.response.send_message("submited", ephemeral=True)


def request_decorate(func):
    async def func_wrapper(bot, channel, user: discord.Member, content, ignore_character: str = "cancel",
                          counter: int = 0):
        if counter > 3:
            await bot.responses.send(channel=channel, make_embed=False, content="Maximum tries. Choosing 0")
            return 0

        if counter == 0:
            content = f"{content}\n*Type <{ignore_character}> to cancel the request*"

        bot_msg = await bot.responses.send(channel=channel, make_embed=False, content=content)

        msg = await bot.wait_for("message", check=lambda m: (m.author == user and m.channel == channel),
                                timeout=40.0)

        if msg.content == ignore_character:
            return None

        await bot_msg.delete()
        await msg.delete()

        if func(msg.content) is not None:
            return func(msg.content)
        else:
            await func_wrapper(bot, channel, user, content, ignore_character, counter+1)

    return func_wrapper

@request_decorate
def request_string(msg) -> str:
    return msg

@request_decorate
def request_url(msg) -> Optional[str]:
    return msg if validators.url(msg) else None

@request_decorate
def request_int(msg) -> Optional[int]:
    try:
        return int(msg)

    except ValueError:
        return None


async def request_emoji(bot, channel, user: discord.Member, content, counter: int = 0) -> Optional[str]:
    if counter > 3:
        await bot.responses.send(channel=channel, make_embed=False, content="Maximum tries. Choosing a random emoji")
        return str(random.choice(bot.emojis))

    bot_msg = await bot.responses.send(channel=channel, make_embed=False, content=content)

    msg: discord.Message = await bot.wait_for("message", check=lambda m: (m.author == user and m.channel == channel),
                                  timeout=40.0)
    content = msg.content
    await bot_msg.delete()
    await msg.delete()

    if emoji.is_emoji(content) or content.strip() in content in [str(i) for i in bot.emojis]:
        return content
    else:
        return None

@request_decorate
def request_bool(content) -> bool:
    if content == "yes" or content == "Yes" or content == "y":
        return True
    elif content == "no" or content == "No" or content == "n":
        return False
    else:
        return None


async def request_roles(bot, channel, user: discord.Member, content, counter: int = 0) -> List[discord.Role]:
    bot_msg = await bot.responses.send(channel=channel, make_embed=False, content=content)

    if counter > 3:
        await bot.responses.send(channel=channel, make_embed=False, content="Maximum tries")
        return []

    msg = await bot.wait_for("message", check=lambda m: (m.author == user and m.channel == channel),
                             timeout=40.0)

    content = msg.content
    roles = msg.role_mentions
    await bot_msg.delete()
    await msg.delete()

    if len(roles) == 0:
        # retry
        return await request_roles(bot, channel, user, content, counter + 1)

    return roles


async def request_channel(bot, channel, user: discord.Member, content, counter: int = 0) -> List[discord.TextChannel]:
    if counter > 3:
        await bot.responses.send(channel=channel, make_embed=False, content="Maximum tries")
        return []

    bot_msg = await bot.responses.send(channel=channel, make_embed=False, content=content)

    msg: discord.Message = await bot.wait_for("message", check=lambda m: (m.author == user and m.channel == channel),
                             timeout=40.0)

    content = msg.content
    channels = msg.channel_mentions
    await bot_msg.delete()
    await msg.delete()

    if len(channels) == 0:
        # retry
        return await request_channel(bot, channel, user, content, counter + 1)

    return channels
