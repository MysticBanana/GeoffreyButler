import asyncio

import discord
from discord.ext import commands
import youtube_dl
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL
from .until import audiomanager, models, commands as audio_commands
from core import botbase
from core.audio import audiocontroller


class YoutubeCog(commands.Cog):
    def __init__(self, bot: botbase.BotBase):
        self.bot: botbase.BotBase = bot

    @commands.command(name="join", help="joins your channel")
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(name="leave", help="leaves the channel again")
    async def leave(self, ctx):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)

        await audio_controller.disconnect()

    @commands.command(name="play", help="plays music/sound from a given link or name")
    async def play(self, ctx, *, url: str):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)
        await audio_commands.play_command(audio_controller, url)
        # audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)
        #
        # audio_controller.queue(track=models.Track(url=url))
        # await audio_controller.play_wrapper()

    @commands.command(name="queue", help="plays music/sound from a given link or name")
    async def queue(self, ctx, *, url: str):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)
        await audio_commands.queue_command(audio_controller, url)

    @commands.command(name="playlist", help="shows the playlist")
    async def playlist(self, ctx):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)

        # todo temp
        await self.bot.responses.send(channel=ctx.channel, content="\n".join([i.url for i in audio_controller.playlist.track_list]))

    @commands.command(name="skip", help="skips current track")
    async def skip(self, ctx):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)
        await audio_commands.skip_command(audio_controller)

    @commands.command(name="prev", help="plays the previous song")
    async def prev(self, ctx):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)
        await audio_commands.prev_command(audio_controller)

    @commands.command(name='pause', help='This command pauses the song')
    async def pause(self, ctx):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)
        await audio_commands.pause_command(audio_controller)

    @commands.command(name='resume', help='Resumes the song')
    async def resume(self, ctx):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)
        await audio_commands.resume_command(audio_controller)


async def setup(bot):
    await bot.add_cog(YoutubeCog(bot))
