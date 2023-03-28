import os, copy, json, sys, enum, dataclasses
from pathlib import Path
import logging
from typing import Dict, List, Any, Tuple


class LoaderType(enum.Enum):
    JSON = "json"
    TXT = ""


class FileHandler:
    @dataclasses.dataclass()
    class Config:
        # saves after setting any value
        auto_save: bool = True
        # if files exists don't overwrite on creation
        exists_ok: bool = True
        loader_type: LoaderType = LoaderType.JSON

    _config: Config = None

    def __init__(self, path: Path = None, config: Config = None, config_type: LoaderType = None):
        self.loader_function = {
            "json": [self.load_json, self.dump_json]
        }

        self._config = config if config else self.Config()
        self._path = path

        self._mode = "r+"
        self._loader_mode = config_type or self.config.loader_type
        self._file_data = None

        # creating path to file if does'nt exists
        path.parent.mkdir(parents=True, exist_ok=self.config.exists_ok)
        path.touch(exist_ok=True)

        self.load_file()

        # todo handle autosave with decorator

    def load_file(self):
        with open(self._path, mode=self._mode, encoding="utf-8") as file:
            content = file.read()

            # if custom loading routine is defined gets loaded
            if self._loader_mode.value in self.loader_function:
                content = self.loader_function[self._loader_mode.value][0](content)
            self._file_data = content

    def flush(self):
        with open(self._path, mode="w", encoding="utf-8") as file:
            content = self._file_data
            if self._loader_mode.value in self.loader_function:
                content = self.loader_function[self._loader_mode.value][1]()

            file.write(content)

    def load_json(self, content: str):
        if not content:
            return dict()
        return json.loads(content)

    def dump_json(self):
        return json.dumps(self._file_data, ensure_ascii=False, indent=4)

    # let you access a json file: FileHandler["somekey"]
    def __getitem__(self, item):
        if isinstance(self._file_data, dict):
            if item in self._file_data:
                return self.content[item]

    def __setitem__(self, key, value):
        if isinstance(self._file_data, dict):
            self._file_data[key] = value

        # saves the new content if autosave
        if self.config.auto_save:
            self.flush()

    def get(self, key, *args):
        if isinstance(self._file_data, dict):
            return self.content.get(key, *args)
        else:
            return self.content

    def set(self, key, *args, **kwargs):
        data = kwargs.get("data", None) or args[0]
        if isinstance(self._file_data, dict):
            self._file_data[key] = data
        else:
            self.content = data

        # saves the new content if autosave
        if self.config.auto_save:
            self.flush()

    def update(self, data: Dict):
        if self.config.loader_type == LoaderType.JSON:
            self._file_data.update(data)

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    @property
    def content(self):
        return copy.deepcopy(self._file_data)

    @content.setter
    def content(self, value):
        self._file_data = value

        # saves the new content if autosave
        if self.config.auto_save:
            self.flush()

    def __str__(self):
        return self._path

