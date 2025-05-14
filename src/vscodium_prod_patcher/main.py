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

from .hooks.main import hooks_main
from .shared import err


def main():
    argv = sys.argv.copy()
    argv.pop(0)
    match argv.pop(0):
        case "hook":
            hooks_main(argv)
        case _:
            err("bad command")
