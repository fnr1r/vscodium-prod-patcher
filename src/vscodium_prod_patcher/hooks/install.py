import os
from pathlib import Path
import sys

from ..config import CONFIG_PATH, get_config
from ..consts import NAME
from .install_templates import HOOK_TARGET_TEMPLATE, HOOK_TEMPLATE
from ..shared import (
    HOOKS_DIR, HOOK_FILE, eprint, pacinfo, text_file_write,
)


USUAL_BIN_PATH = Path("/usr/bin") / NAME


def get_bin_path() -> Path:
    bin_path = Path(sys.argv[0])
    if bin_path != USUAL_BIN_PATH:
        eprint("Warning:", NAME, "binary is in a non-standard path:", bin_path)
    return bin_path.absolute()


def hook_install():
    config = get_config()
    packages: dict[str, str] = config["packages"]
    if not packages:
        if HOOK_FILE.exists():
            os.remove(HOOK_FILE)
        pacinfo(
            "No VSCodium package defined.",
            f"Try to configure {NAME} by creating",
            CONFIG_PATH,
        )
        return
    targets = "\n".join([
        HOOK_TARGET_TEMPLATE.format(pkg=pkg)
        for pkg in packages.keys()
    ])
    bin_path = get_bin_path()
    hook_contents = HOOK_TEMPLATE.format(
        bin=bin_path,
        name=NAME, targets=targets,
    )
    HOOKS_DIR.mkdir(parents=True, exist_ok=True)
    text_file_write(HOOK_FILE, hook_contents)
