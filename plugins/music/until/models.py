import random
from dataclasses import dataclass
from typing import Any, Dict, Tuple, Callable, Optional
from collections import deque, defaultdict
from core.audio import models
from . import util
import discord
import youtube_dl

youtube_dl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}


class Track(models.Track):
    @dataclass
    class SongInfo:
        uploader: str
        title: str
        duration: str
        webpage_url: str
        thumbnail: Any = None

    def __init__(self, *args, **kwargs):
        super(Track, self).__init__(*args, **kwargs)

        # todo url might be a name

        if not util.is_url(self.url):
            self.url = self.find_track(self.url)

        self.info = self.SongInfo(kwargs.get("uploader"),
                                  kwargs.get("title"),
                                  kwargs.get("duration"),
                                  kwargs.get("webpage_url"),
                                  kwargs.get("thumbnail"))

    def get_track_info(self, url, **kwargs):

        def extract(d):
            try:
                return d.extract_info(url, download=False)

            except Exception as e:
                return

        if len(kwargs) == 0:
            kwargs = youtube_dl_format_options

        try:
            downloader = youtube_dl.YoutubeDL(kwargs)

        except Exception:
            kwargs.pop("format")
            downloader = youtube_dl.YoutubeDL(kwargs)

        return extract(downloader)

    def find_track(self, name):
        if util.is_url(name) is not None:
            return name

        with youtube_dl.YoutubeDL(youtube_dl_format_options) as ydl:
            info = ydl.extract_info(name, download=False)

        # todo might make a selection for user to select other versions of the song?
        return None if info is None else f"https://www.youtube.com/watch?v={info['entries'][0]['id']}"

    def load(self):
        """loads additional information for track"""

        if self.loaded:
            return

        track = self.get_track_info(self.url)

        thumbnail = track.get("thumbnails", None)
        thumbnail = None if thumbnail is None else thumbnail[-1]["url"]

        self.url = track.get("url")
        self.info.uploader = track.get("uploader")
        self.info.title = track.get("title")
        self.info.duration = track.get("duration")
        self.info.webpage_url = track.get("webpage_url")
        self.info.thumbnail = thumbnail

    async def send_interface(self, bot, channel: discord.TextChannel):
        """sends a message in a channel to interact with (track play interface)
        Important:
            - Use the bot MessageController to send messages"""

        await bot.responses.send(channel=channel, make_embed=False, content=f"Playing song: {self.info.title}")


class Playlist:

    # stores a settings prototype for all playlists
    @dataclass
    class Settings:
        max_queue_length: int = 50
        max_history_length: int = 100

        save_history: bool = True
        loop: bool = False

    track_playlist: deque[Track]
    track_history: deque[Track]

    def __init__(self, settings: Settings = Settings()):
        self.track_playlist = deque()
        self.track_history = deque()

        self.track_history_pair = {}

        self.settings = settings

    def __len__(self):
        return len(self.track_playlist)

    def add(self, track: Track):
        if len(self.track_playlist) > self.settings.max_queue_length:
            return
        self.track_playlist.append(track)

    def prev(self, current_track: Track = None) -> Optional[Track]:

        if len(self.track_history) == 0:
            return None

        if current_track is None:
            self.track_playlist.appendleft(self.track_history[-1])
            return self.track_playlist[0]

        ind = self.track_history.index(current_track)
        self.track_playlist.appendleft(self.track_history[ind - 1])

        # no idea why but maybe needed
        self.track_playlist.insert(1, current_track)

    def next(self, track_played: Track = None) -> Optional[Track]:
        if self.settings.loop:
            self.track_playlist.appendleft(self.track_history[-1])

        if len(self.track_playlist) == 0:
            return None

        if len(self.track_history) > self.settings.max_history_length:
            self.track_history.popleft()

        return self.track_playlist[0]

    def shuffle(self):
        random.shuffle(self.track_playlist)

    def move(self, old_index: int, new_index: int):
        temp = self.track_playlist[old_index]
        del self.track_playlist[old_index]
        self.track_playlist.insert(new_index, temp)

    def empty(self):
        self.track_playlist.clear()
        self.track_history.clear()