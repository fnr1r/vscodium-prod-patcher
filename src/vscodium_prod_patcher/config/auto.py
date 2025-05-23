from copy import deepcopy
from typing import Any, Optional

from ..shared import eprint
from .main import save_config
from .template import CONFIG_TEMPLATE
from .utils import list_vscodium_packages, try_guess_editor_path


def autoinfo(*args: object, **kwargs):
    print(":: autoconf:", *args, **kwargs)


def autoerr(*args: object, **kwargs):
    eprint(":: autoconf failed:", *args, **kwargs)


def try_autoconf() -> Optional[dict[str, Any]]:
    """
    Oh, look! It's AI!!!
    """
    config = deepcopy(CONFIG_TEMPLATE)
    conf_packages = config["packages"]
    packages = list_vscodium_packages()
    if not packages:
        autoerr("not VSCodium packages detected")
        return None
    if len(packages) > 1:
        autoerr("too many VSCodium packages detected")
        return None
    pkg = packages.pop()
    autoinfo("VSCodium package:", pkg)
    editor_path = try_guess_editor_path(pkg)
    if editor_path is None:
        autoerr("editor path not detected")
        return None
    autoinfo("Editor path:", editor_path)
    conf_packages[pkg] = str(editor_path)
    autoinfo("Auto-configured with default patch settings")
    save_config(config)
    return config
