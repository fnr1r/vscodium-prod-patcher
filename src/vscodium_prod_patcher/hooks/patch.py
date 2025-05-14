import sys

from ..patch import patch_pkgs


def hook_patch():
    changed_packages = [
        str(line).strip()
        for line in sys.stdin
    ]
    if not changed_packages:
        return
    patch_pkgs(changed_packages)
