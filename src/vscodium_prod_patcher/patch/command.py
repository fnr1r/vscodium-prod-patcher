from ..patch import patch_pkg
from ..shared import err
from ..utils.backup import backup_editor_data, restore_editor_data

PATCH_SUBCMDS = ["apply", "backup", "restore"]


def patch_apply(package_name: str, from_backup: bool):
    patch_pkg(package_name, from_backup=from_backup)


def patch_backup(package_name: str):
    backup_editor_data(package_name)


def patch_restore(package_name: str):
    restore_editor_data(package_name)


def patch_main(args):
    match args.subcommand:
        case "apply":
            patch_apply(args.package_name, args.from_backup)
        case "backup":
            patch_backup(args.package_name)
        case "restore":
            patch_restore(args.package_name)
        case _:
            err("bad subcommand")
