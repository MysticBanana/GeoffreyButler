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

        if self.bot.get("audio_controller") is not None:
            raise AudioControllerExists("You try to create a new controller but there is already a "
                                        "controller for this guild")

        self.default_voice_channel: discord.VoiceChannel = None
        self.default_text_channel: discord.TextChannel = None

        self.playlist = models.Playlist()

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

    async def play_track(self, track: models.Track):

        if track.url is None:
            return

        if self.default_voice_channel is None:
            return

        await self.connect()

        if self.guild.voice_client.is_playing():
            return

        self.guild.voice_client.play(discord.FFmpegPCMAudio(
            track.url, before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'),
            after=lambda event: self.on_next(event)
        )
        self.guild.voice_client.is_playing()

        # todo add preloading for other tracks here

    async def play_wrapper(self, track: models.Track, voice_channel: discord.VoiceChannel = None,
                           text_channel: discord.TextChannel = None):
        """
        Wrapper funtion that calls play_track
        :param text_channel:
        :param voice_channel:
        :param track: track to play
        """

        # loads additional informations about a track
        track.load()

        if self.default_voice_channel is not None and voice_channel is not None\
                and self.default_voice_channel != voice_channel:
            # todo handling of wrong channel
            # send a message here maybe
            return

        self.default_voice_channel = voice_channel
        self.default_text_channel = text_channel if text_channel is not None else self.default_text_channel

        await self.play_track(track)

        # sending a status message in chat (interface)
        await track.send_interface(self.bot, self.default_text_channel)

    async def on_next(self, event):
        """Gets called when a track ended"""

        await self.play_wrapper(self.playlist.next())

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




