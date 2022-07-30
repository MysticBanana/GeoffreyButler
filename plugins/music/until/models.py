import random
from dataclasses import dataclass
from typing import Any, Dict, Tuple, Callable, Optional
from collections import deque, defaultdict


class Song:
    @dataclass
    class SongInfo:
        uploader: str
        title: str
        duration: str
        webpage_url: str
        thumbnail: Any = None

    base_url: str
    info: SongInfo

    def __init__(self, base_url: str = "", uploader: str = "", title: str = "", duration: str = "", webpage_url: str = "",
                 thumbnail=None, **kwargs):
        self.base_url = base_url
        self.info = self.SongInfo(uploader, title, duration, webpage_url, thumbnail)


class Playlist:

    # stores a settings prototype for all playlists
    @dataclass
    class Settings:
        max_queue_length: int = 50
        max_history_length: int = 100

        save_history: bool = True
        loop: bool = False

    track_playlist: deque[Song]
    track_history: deque[Song]

    settings: Settings

    def __init__(self, settings: Settings = Settings()):
        self.track_playlist = deque()
        self.track_history = deque()

        self.track_history_pair = {}

        self.settings = settings

    def __len__(self):
        return len(self.track_playlist)

    def add(self, track: Song):
        if len(self.track_playlist) > self.settings.max_queue_length:
            return
        self.track_playlist.append(track)

    def prev(self, current_track: Song = None) -> Optional[Song]:

        if len(self.track_history) == 0:
            return None

        if current_track is None:
            self.track_playlist.appendleft(self.track_history[-1])
            return self.track_playlist[0]

        ind = self.track_history.index(current_track)
        self.track_playlist.appendleft(self.track_history[ind - 1])

        # no idea why but maybe needed
        self.track_playlist.insert(1, current_track)

    def next(self, track_played: Song = None) -> Optional[Song]:
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