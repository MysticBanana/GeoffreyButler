from typing import Optional, Tuple, Union, Dict, List, Any
import discord


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


async def request_string(bot, channel, user: discord.Member, content):
    await bot.responses.send(channel=channel, make_embed=False, content=content)

    msg = await bot.wait_for("message", check=lambda m: (m.author == user and m.channel == channel),
                                  timeout=40.0)

    return msg.content


async def request_roles(bot, channel, user: discord.Member, content) -> List[discord.Role]:
    await bot.responses.send(channel=channel, make_embed=False, content=content)

    msg = await bot.wait_for("message", check=lambda m: (m.author == user and m.channel == channel),
                             timeout=40.0)

    return msg.role_mentions