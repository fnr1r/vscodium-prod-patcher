from .main import save_config
from .paths import CONFIG_PATH
from .template import CONFIG_TEMPLATE
from ..shared import err


def config_default():
    if CONFIG_PATH.exists():
        err("can't overwrite config with default file")
    save_config(CONFIG_TEMPLATE)


def config_main(args):
    match args.subcommand:
        case "default":
            config_default()
        case _:
            err("invalid config type")
