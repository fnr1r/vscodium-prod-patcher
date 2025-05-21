from ..utils.backup import backup_editor_data, restore_editor_data
from ..config import get_config
from ..patch import patch_pkg
from ..shared import err

PATCH_SUBCMDS = ["apply", "backup", "restore"]


def patch_apply(package_name: str):
    config = get_config()
    editor_config = config.packages[package_name]
    patch_pkg(editor_config, config)


def patch_backup(package_name: str):
    backup_editor_data(package_name)


def patch_restore(package_name: str):
    restore_editor_data(package_name)


def patch_main(args):
    match args.subcommand:
        case "apply":
            patch_apply(args.editor_path)
        case "backup":
            patch_apply(args.editor_path)
        case "restore":
            patch_restore(args.editor_path)
        case _:
            err("bad subcommand")
