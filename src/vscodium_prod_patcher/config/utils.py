import re
from copy import deepcopy
from pathlib import Path
from typing import Optional

from ..consts import NAME
from ..pacman.minipacman import MiniPacman
from .schema import VscEditorMetaConfig, VscPatchConfig

INSTALL_BASE_PATHS = ["/usr/share", "/usr/lib", "/opt"]
PRODUCT_JSON_SUFFIXES = [
    "resources/app/product.json",
    "product.json",
]


def merge_patch_config(
    base: VscPatchConfig,
    override: Optional[VscPatchConfig],
) -> VscPatchConfig:
    if override is None:
        return base
    new = deepcopy(base)
    if override.data_dir is not None:
        new.data_dir = override.data_dir
    if override.extension_source is not None:
        new.extension_source = override.extension_source
    if override.extra_features is not None:
        new.extra_features = override.extra_features
    return new


def list_vscodium_packages(exclude_debug: bool = True) -> list[str]:
    vscodium_regex = re.compile(r"^(vs)?codium\S*$")
    packages = MiniPacman().list_packages()
    packages = list(filter(vscodium_regex.match, packages))
    packages.remove(NAME)
    if exclude_debug:
        def no_debug(pkg: str) -> bool:
            return not pkg.endswith("-debug")
        packages = list(filter(no_debug, packages))
    return packages


def try_guess_editor_path(pkg: str) -> Optional[Path]:
    for install_base_path in INSTALL_BASE_PATHS:
        path = Path(install_base_path) / pkg
        if not path.exists():
            continue
        return path
    return None


def try_product_json_path_from_editor_path(
    editor_path: Path,
) -> Optional[Path]:
    for suffix in PRODUCT_JSON_SUFFIXES:
        product_json_path = editor_path / suffix
        if not product_json_path.exists():
            continue
        return product_json_path
    return None


def try_product_json_from_pkg_files(
    pkg_files: list[str],
) -> Optional[Path]:
    pkg_files_p = [
        Path(path)
        for path in pkg_files
    ]
    product_json_files = [
        path
        for path in pkg_files_p
        if path.name == "product.json"
    ]
    if len(product_json_files) != 1:
        return None
    return Path("/") / product_json_files[0]


def try_editor_path_from_product_json(
    product_json_path: Path,
) -> Optional[Path]:
    product_json = str(product_json_path)
    for suffix in PRODUCT_JSON_SUFFIXES:
        editor_str = product_json.removesuffix(suffix)
        if editor_str == product_json:
            continue
        return Path(editor_str)
    return None


def try_guess_editor_meta(pkg: str) -> Optional[VscEditorMetaConfig]:
    pacman = MiniPacman()
    pkg_files = pacman.package_files(pkg)

    editor_path = None
    product_json_path = None

    # New method
    product_json_path = try_product_json_from_pkg_files(pkg_files)
    if product_json_path is not None:
        editor_path = try_editor_path_from_product_json(product_json_path)

    # Old method
    if editor_path is None:
        editor_path = try_guess_editor_path(pkg)
    if product_json_path is None and editor_path is not None:
        product_json_path = try_product_json_path_from_editor_path(
            editor_path,
        )

    if editor_path is None:
        return None
    if product_json_path is None:
        return None

    editor_str = str(editor_path)
    product_json_str = str(product_json_path)
    product_json_str = product_json_str.removeprefix(editor_str + "/")
    product_json_path = Path(product_json_str)

    return VscEditorMetaConfig(editor_path, product_json_path)
