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

from .config.command import config_main
from .hooks.main import hooks_main
from .patch.command import patch_main
from .shared import err


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    parser_config = subparsers.add_parser("config")
    parser_config.add_argument("subcommand")
    parser_hook = subparsers.add_parser("hook", help="Run a hook")
    parser_hook.add_argument("name", help="Hook name")
    parser_patch = subparsers.add_parser(
        "patch", help="Manually patch a VSCodium installation",
    )
    parser_patch.add_argument(
        "editor_path", type=Path,
        help="installation path",
    )
    args = parser.parse_args()
    match args.command:
        case "config":
            config_main(args)
        case "hook":
            hooks_main(args)
        case "patch":
            patch_main(args)
        case _:
            err("bad command")
