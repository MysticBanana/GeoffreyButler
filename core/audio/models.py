import random
from dataclasses import dataclass
from typing import Any, Dict, Tuple, Callable, Optional
from collections import deque, defaultdict
import discord
import time


class Track:
    url: str
    loaded: bool

    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.loaded = False

    def load(self):
        """loads additional information for track"""
        pass

    def convert_time(self, seconds):
        return time.strftime("%H:%M:%S", time.gmtime(seconds))

    async def send_interface(self, bot, channel: discord.TextChannel):
        """sends a message in a channel to interact with (track play interface)
        Important:
            - Use the bot MessageController to send messages"""


class Playlist:

    @dataclass
    class Settings:
        max_queue_length: int = 50
        max_history_length: int = 100

        save_history: bool = True
        loop: bool = False

    # playlist what to play next
    track_list: deque[Track]

    # list of all tracks played
    track_history: deque[Track]

    # playlist settings
    settings: Settings

    def __init__(self, settings: Settings = Settings()):
        self.track_list = deque()
        self.track_history = deque()

        self.settings = settings

    @property
    def current_track(self) -> Optional[Track]:
        if not len(self.track_list) > 0:
            return None
        return self.track_list[0]

    @property
    def previous_track(self) -> Optional[Track]:
        if len(self.track_history) > 0:
            return None
        return self.track_history[-1]

    def next(self) -> Track:
        self.track_history.append(self.track_list.popleft())

        if len(self.track_history) > self.settings.max_history_length:
            self.track_history.popleft()

        return self.current_track

    def prev(self) -> Track:
        self.track_list.appendleft(self.track_history.pop())

        if len(self.track_list) > self.settings.max_queue_length:
            self.track_list.pop()

        return self.current_track

    def add(self, track: Track) -> bool:
        if len(self.track_list) > self.settings.max_queue_length:
            return False

        self.track_list.append(track)

        return True

    def clear(self):
        self.track_list.clear()
        self.track_history.clear()




