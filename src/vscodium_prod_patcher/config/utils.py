import re
from pathlib import Path
from typing import Optional

from ..consts import NAME
from ..pacman import pacman_list_packages

INSTALL_BASE_PATHS = ["/usr/share", "/opt"]


def list_vscodium_packages() -> list[str]:
    vscodium_regex = re.compile(r"^(vs)?codium\S*$")
    packages = pacman_list_packages()
    return [
        pkg
        for pkg in packages
        if vscodium_regex.match(pkg) and pkg != NAME
    ]


def try_guess_editor_path(pkg: str) -> Optional[Path]:
    for install_base_path in INSTALL_BASE_PATHS:
        path = Path(install_base_path) / pkg
        if not path.exists():
            continue
        return path
    return None
