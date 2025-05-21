import os

from ..hooks.install import write_update_hook_cfg
from ..shared import eprint, err
from ..utils.editor import EditorWrap
from .auto import try_autoconf
from .main import get_config, save_config
from .paths import CONFIG_PATH
from .schema import Config

CONFIG_SUBCMDS = ["auto", "default", "edit", "features", "packages"]


def config_default():
    if CONFIG_PATH.exists():
        err("can't overwrite config with default file")
    save_config(Config())


def config_edit():
    changed = EditorWrap().edit_file_as_root(CONFIG_PATH)
    if not changed:
        eprint("No changes! Will not update hook.")
        return
    if os.getuid() != 0:
        eprint("Skipping install hook update")
        return
    write_update_hook_cfg(get_config(force_reload=True))


# This is required because inquirer is optional
# pylint: disable=import-outside-toplevel
def config_main(args):
    match args.subcommand:
        case "auto":
            try_autoconf()
        case "default":
            config_default()
        case "edit":
            config_edit()
        case "features":
            from .tui import config_features
            config_features()
        case "packages":
            from .tui import config_packages
            config_packages()
        case _:
            err("invalid config type")
