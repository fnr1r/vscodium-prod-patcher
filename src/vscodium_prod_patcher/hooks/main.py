from .install import hook_install
from .patch import hook_patch
from ..shared import err


def hooks_main(argv: list[str]):
    match argv.pop(0):
        case "install":
            hook_install()
        case "patch":
            hook_patch()
        case _:
            err("invalid hook")
