from typing import Optional

from ..shared import eprint
from .main import save_config
from .schema import Config, VscEditorConfig
from .utils import list_vscodium_packages, try_guess_editor_meta


def autoinfo(*args: object, **kwargs):
    print(":: autoconf:", *args, **kwargs)


def autoerr(*args: object, **kwargs):
    eprint(":: autoconf failed:", *args, **kwargs)


def try_autoconf() -> Optional[Config]:
    """
    Oh, look! It's AI!!!
    """
    config = Config()
    conf_packages = config.packages
    packages = list_vscodium_packages()
    if not packages:
        autoerr("not VSCodium packages detected")
        return None
    if len(packages) > 1:
        autoerr("too many VSCodium packages detected")
        return None
    pkg = packages.pop()
    autoinfo("VSCodium package:", pkg)
    meta = try_guess_editor_meta(pkg)
    if meta is None:
        autoerr("editor metadata not detected")
        return None
    autoinfo("Editor path:", meta.editor_path)
    autoinfo("product.json subpath:", meta.product_json_path)
    editor_info = VscEditorConfig(meta, None)
    conf_packages[pkg] = editor_info
    autoinfo("Auto-configured with default patch settings")
    save_config(config)
    return config
