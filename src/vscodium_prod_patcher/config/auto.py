from typing import Optional

from ..pacman.minipacman import MiniPacman
from ..utils.print import pacinfo, pacwarn
from .main import save_config
from .schema import Config, VscEditorConfig
from .utils import list_vscodium_packages, try_guess_editor_meta


def autoerr(*args: object, **kwargs):
    print("!!> automatic configuration failed!")
    pacwarn(*args, **kwargs)


def try_autoconf() -> Optional[Config]:
    """
    Oh, look! It's AI!!!
    """
    config = Config()
    conf_packages = config.packages
    packages = list_vscodium_packages()
    if not packages:
        autoerr("no VSCodium packages detected")
        return None
    pacinfo("VSCodium packages:", len(packages))
    info = MiniPacman().get_package_info()
    for pkg in packages:
        try:
            pkginfo = info[pkg]
        except KeyError:
            pacwarn(" ", pkg, "has no info???")
            continue
        pacinfo(pkg, pkginfo.version)
        meta = try_guess_editor_meta(pkg)
        if meta is None:
            pacwarn(" ", "editor metadata not detected")
            continue
        pacinfo(" ", "Editor path:", meta.editor_path)
        pacinfo(" ", "product.json path:", meta.abs_product_json_path)
        editor_info = VscEditorConfig(meta, None)
        conf_packages[pkg] = editor_info
    if not conf_packages:
        autoerr("no actual VSCodium packages seem to be installed")
        return None
    pacinfo("Auto-configured with default patch settings")
    save_config(config)
    return config
