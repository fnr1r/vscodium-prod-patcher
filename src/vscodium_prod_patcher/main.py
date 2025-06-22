"""
vscodium-prod-patcher by fnrir

I'm tired of having multiple versions of different "patchers" for different
versions of VSCodium. So fuck it. This one is configurable and universal.

I might add backups later. rn i'm tired

trans rights are human rights

polska gurom

GitHub: <https://github.com/fnr1r>
Matrix: @fnrir:matrix.org
Mastodon: <https://tech.lgbt/@fnrir>
Mail: fnr1r0@protonmail.com
Credit Card: 5809820978480085 Date: 06/21 CVC: 420
IP address: [::1]
"""

from argparse import ArgumentParser
from pathlib import Path

from .config.command import CONFIG_SUBCMDS, config_main
from .hooks.main import hooks_main
from .pacman.minipacman import set_pacman_conf_path
from .patch.command import patch_main
from .shared import err


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--pacman-config",
        default="/etc/pacman.conf",
        type=Path,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    parser_config = subparsers.add_parser("config")
    subp_config = parser_config.add_subparsers(
        dest="subcommand",
        required=True,
    )
    for subcmd in CONFIG_SUBCMDS:
        subp_config.add_parser(subcmd)
    parser_hook = subparsers.add_parser("hook", help="Run a hook")
    parser_hook.add_argument("name", help="Hook name")
    parser_patch = subparsers.add_parser(
        "patch", help="Manually patch a VSCodium installation",
    )
    subp_patch = parser_patch.add_subparsers(
        dest="subcommand",
        required=True,
    )
    patch_cmds = [
        subp_patch.add_parser(subcmd)
        for subcmd in ["backup", "restore"]
    ]
    patch_apply = subp_patch.add_parser("apply")
    patch_apply.add_argument(
        "--from-backup",
        default=True,
        type=bool,
    )
    patch_cmds.append(patch_apply)
    for patch_cmd in patch_cmds:
        patch_cmd.add_argument(
            "package_name",
            help="package name",
        )
    args = parser.parse_args()
    set_pacman_conf_path(args.pacman_config)
    match args.command:
        case "config":
            config_main(args)
        case "hook":
            hooks_main(args)
        case "patch":
            patch_main(args)
        case _:
            err("bad command")
