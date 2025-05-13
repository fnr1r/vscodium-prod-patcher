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

import sys

from .hook import install_hook
from .patch import patch_pkgs
from .shared import err


def main():
    match sys.argv[1]:
        case "hook":
            install_hook()
        case "patch":
            patch_pkgs()
        case _:
            err("bad command")
