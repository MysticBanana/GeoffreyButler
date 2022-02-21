from discord.ext import commands
import discord

class DatabaseManagerRPG:
    pass

class RPG:

    def __init__(self, bot):
        self.bot = bot
        self.messageNumber = 1
        self.user = None

    async def start(self, user):
        self.user = user
        message = "test"  # TODO: database first message
        self.messageNumber = self.messageNumber + 1
        await DirectMessage.sendDM(self, self.user, self.bot, message)

    def reset(self):
        self.messageNumber = 1
        self.user = None

class DirectMessage:

    async def sendDM(self, user, bot, message):
        await bot.send_message(user, message)

    def recieveDM(self):
        messageInfo = []
        # TODO: get message

# if __name__ == "__main__":
#     rpg = RPG("a")
#     rpg.start("al")
#     rpg.reset()