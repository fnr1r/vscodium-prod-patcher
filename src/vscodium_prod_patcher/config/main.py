import os
from pathlib import Path
from typing import Any, Optional

import toml

from ..consts import ENCODING
from .paths import CONFIG_DIR, CONFIG_PATH
from .schema import Config

CONFIG: Optional[Config] = None

EXTENSION_SOURCES = ["openvsx", "microsoft"]


def toml_load(path: Path):
    with open(path, "rt", encoding=ENCODING) as file:
        return toml.load(file)


def toml_save(path: Path, obj: Any):
    with open(path, "wt", encoding=ENCODING) as file:
        toml.dump(obj, file)


def load_config() -> Config:
    try:
        return Config.from_dict(toml_load(CONFIG_PATH))
    except FileNotFoundError:
        return Config()


def get_config() -> Config:
    # pylint: disable=W0603
    global CONFIG
    if CONFIG is None:
        CONFIG = load_config()
    return CONFIG


def save_config(config: Config):
    # pylint: disable=W0603
    global CONFIG
    CONFIG = config
    os.makedirs(CONFIG_DIR, exist_ok=True)
    toml_save(CONFIG_PATH, config.to_dict())
