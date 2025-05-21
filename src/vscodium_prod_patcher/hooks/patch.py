import sys

from ..patch import patch_pkgs
from ..utils.backup import backup_editor_data


def hook_patch():
    changed_packages = [
        str(line).strip()
        for line in sys.stdin
    ]
    if not changed_packages:
        return
    for pkg in changed_packages:
        backup_editor_data(pkg)
    patch_pkgs(changed_packages)
