from pathlib import Path

from .consts import NAME

DATA_DIR = Path(__file__).parent

BASE_CONFIG_DIR = Path("/etc")
BASE_VAR_LIB_DIR = Path("/var/lib")

HOOKS_DIR = BASE_CONFIG_DIR / "pacman.d/hooks"
HOOK_FILE = HOOKS_DIR / f"98-{NAME}-action.hook"

DB_DIR = BASE_VAR_LIB_DIR / NAME
BACKUPS_DIR = DB_DIR / "backups"
