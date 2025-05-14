from pathlib import Path
import sys

from ..config import get_config
from ..patch import patch_pkg


def hook_patch():
    changed_packages = [
        str(line).strip()
        for line in sys.stdin
    ]
    if not changed_packages:
        return
    config = get_config()
    packages: dict[str, str] = config["packages"]
    changed_packages = [
        pkg
        for pkg in changed_packages
        if pkg in packages.keys()
    ]
    patch_config = config["patch"]
    for pkg in changed_packages:
        patch_pkg(pkg, Path(packages[pkg]), patch_config)
