import os

from .config import CONFIG_PATH, get_config
from .consts import NAME
from .hook_templates import HOOK_TARGET_TEMPLATE, HOOK_TEMPLATE
from .shared import (
    HOOKS_DIR, HOOK_FILE, pacinfo, text_file_write,
)


def install_hook():
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
    hook_contents = HOOK_TEMPLATE.format(
        name=NAME, targets=targets,
    )
    HOOKS_DIR.mkdir(parents=True, exist_ok=True)
    text_file_write(HOOK_FILE, hook_contents)
