import asyncio

import discord
from discord.ext import commands
import youtube_dl
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL
from .until import audiomanager, models
from core import botbase
from core.audio import audiocontroller


class YoutubeCog(commands.Cog):
    def __init__(self, bot: botbase.BotBase):
        self.bot: botbase.BotBase = bot

    @commands.command(name="join", description="joins your channel")
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(name="leave", description="leaves the channel again")
    async def leave(self, ctx):
        pass

    @commands.command(name="play", description="plays music/sound from a given link or name")
    async def play(self, ctx, *, url: str):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)

        audio_controller.queue(track=models.Track(url=url))
        await audio_controller.play_wrapper()

    @commands.command(name="playlist", description="shows the playlist")
    async def playlist(self, ctx):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)

        # todo temp
        await self.bot.responses.send(channel=ctx.channel, content="\n".join([i.url for i in audio_controller.playlist.track_list]))

    @commands.command(name="skip", description="skips current track")
    async def skip(self, ctx):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)
        audio_controller.guild.voice_client.stop()

        audio_controller.on_next()

    @commands.command(name="play2", description="plays music/sound from a given link or name")
    async def play2(self, ctx, url):
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('Bot is playing')

    @commands.command(name='pause', help='This command pauses the song')
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='resume', help='Resumes the song')
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command")


async def setup(bot):
    await bot.add_cog(YoutubeCog(bot))
