import json
import sys
from pathlib import Path
from typing import Any

from .consts import ENCODING, NAME

BASE_CONFIG_DIR = Path("/etc")

HOOKS_DIR = BASE_CONFIG_DIR / "pacman.d/hooks"
HOOK_FILE = HOOKS_DIR / f"98-{NAME}-action.hook"

DATA_DIR = Path(__file__).parent


def eprint(*args: object, **kwargs):
    "Prints to stderr"
    print(*args, file=sys.stderr, **kwargs)


def pacinfo(*args: object, **kwargs):
    print("::", *args, **kwargs)


def err(*args: object, exit_code=1, **kwargs):
    eprint(*args, **kwargs)
    sys.exit(exit_code)


def text_file_write(path: Path, txt: str):
    with open(path, "wt", encoding=ENCODING) as file:
        file.write(txt)


def json_load(path: Path):
    with open(path, "rt", encoding=ENCODING) as file:
        return json.load(file)


def json_write(path: Path, obj: Any, *args, **kwargs):
    with open(path, "wt", encoding=ENCODING) as file:
        json.dump(obj, file, *args, **kwargs)
