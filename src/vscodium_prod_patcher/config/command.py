from ..shared import err
from .auto import try_autoconf
from .main import save_config
from .paths import CONFIG_PATH
from .template import CONFIG_TEMPLATE


def config_default():
    if CONFIG_PATH.exists():
        err("can't overwrite config with default file")
    save_config(CONFIG_TEMPLATE)


# This is required because inquirer is optional
# pylint: disable=import-outside-toplevel
def config_main(args):
    match args.subcommand:
        case "auto":
            try_autoconf()
        case "default":
            config_default()
        case "features":
            from .tui import config_features
            config_features()
        case "packages":
            from .tui import config_packages
            config_packages()
        case _:
            err("invalid config type")
