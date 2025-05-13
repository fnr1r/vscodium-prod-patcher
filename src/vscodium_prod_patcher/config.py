from pathlib import Path
from typing import Any, Optional

import toml

from .config_templates import CONFIG_TEMPLATE
from .consts import ENCODING, NAME
from .shared import BASE_CONFIG_DIR


CONFIG_DIR = BASE_CONFIG_DIR / NAME
CONFIG_PATH = CONFIG_DIR / "config.toml"

CONFIG: Optional[dict[str, Any]] = None

EXTENSION_SOURCES = ["openvsx", "microsoft"]


def toml_load(path: Path):
    with open(path, "rt", encoding=ENCODING) as file:
        return toml.load(file)


def load_config():
    try:
        return toml_load(CONFIG_PATH)
    except FileNotFoundError:
        return CONFIG_TEMPLATE


def get_config() -> dict[str, Any]:
    # pylint: disable=W0603
    global CONFIG
    if CONFIG is None:
        CONFIG = load_config()
    return CONFIG
