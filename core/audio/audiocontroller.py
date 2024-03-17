from . import models
import discord
from typing import List
from .exceptions import AudioControllerExists


class Controller:

    guild: discord.Guild
    _guilds: List[discord.Guild]

    # thats true if bot is playing a track
    is_playing = False

    playlist: models.Playlist

    def __init__(self, bot, guild: discord.Guild):
        self.bot = bot
        self.guild = guild

        if guild in self.bot.audio_controller:
            raise AudioControllerExists("You try to create a new controller but there is already a "
                                        "controller for this guild")

        self.default_voice_channel: discord.VoiceChannel = None
        self.default_text_channel: discord.TextChannel = None

        self.playlist = models.Playlist()

    @property
    def current_track(self) -> models.Track:
        return self.playlist.current_track

    @property
    def guilds(self) -> List[discord.Guild]:
        return Controller._guilds

    @guilds.setter
    def guilds(self, value):
        Controller._guilds = value

    @property
    def text_channel(self):
        return self.default_text_channel

    @text_channel.setter
    def text_channel(self, value):
        self.default_text_channel = value

    @property
    def voice_channel(self):
        return self.default_voice_channel

    @voice_channel.setter
    def voice_channel(self, value):
        self.default_voice_channel = value

    @staticmethod
    async def controller_from_ctx(bot, ctx) -> "Controller":
        audio_controller = bot.get_audio_controller(ctx.guild)

        audio_controller.text_channel = ctx.channel

        if not ctx.author.voice:
            await bot.responses.send(channel=ctx.channel, make_embed=False, content="You arn't in a voice channel")

        audio_controller.voice_channel = ctx.author.voice.channel

        return audio_controller

    @staticmethod
    async def controller_from_interaction(bot, interaction: discord.Interaction) -> "Controller":
        audio_controller = bot.get_audio_controller(interaction.guild)

        audio_controller.text_channel = interaction.channel

        if not interaction.user.voice:
            await bot.responses.send(channel=interaction.channel,
                                     make_embed=False,
                                     content="You arn't in a voice channel")

        audio_controller.voice_channel = interaction.user.voice.channel

        return audio_controller

    def queue(self, track: models.Track):
        if track is not None:
            self.playlist.add(track)

        print(self.playlist.track_list)

    async def play_track(self, track: models.Track):

        if track.url is None:
            return

        if self.default_voice_channel is None:
            return

        await self.connect(self.default_voice_channel)

        if self.guild.voice_client.is_playing():
            return

        self.guild.voice_client.play(discord.FFmpegPCMAudio(
            track.url, before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'),
            after=lambda event: self.on_next(event)
        )
        self.guild.voice_client.is_playing()

        # todo add preloading for other tracks here

    async def play_wrapper(self, track: models.Track = None, voice_channel: discord.VoiceChannel = None,
                           text_channel: discord.TextChannel = None):
        """
        Wrapper funtion that calls play_track
        :param text_channel:
        :param voice_channel:
        :param track: track to play
        """

        if track is None:
            if len(self.playlist.track_list) == 0:
                return

            track = self.playlist.current_track

        # loads additional informations about a track
        track.load()

        if self.default_voice_channel is None:
            if voice_channel is None:
                return
            else:
                if self.default_voice_channel != voice_channel:
                    return
                self.default_voice_channel = voice_channel

        self.default_text_channel = text_channel if text_channel is not None else self.default_text_channel

        await self.play_track(track)

        # sending a status message in chat (interface)
        # await track.send_interface(self.bot, self.default_text_channel)

    def on_next(self, event=None):
        """Gets called when a track ended"""

        if len(self.playlist.track_list) == 0:
            return

        coro = self.play_wrapper(self.playlist.next())
        self.bot.loop.create_task(coro)

    async def connect(self, channel: discord.VoiceChannel = None) -> bool:
        if channel is None:
            return False

        if self.guild.voice_client is None:
            await channel.connect(reconnect=True)

        return True

    async def disconnect(self):
        await self.stop_player()
        await self.guild.voice_client.disconnect(force=True)

    async def stop_player(self):
        if self.guild.voice_client is None:
            return

        self.playlist.track_list.clear()
        self.guild.voice_client.stop()




