from contextlib import suppress
from pathlib import Path
from typing import Any

from ..config.main import get_config
from ..shared import DATA_DIR, json_load, json_write, pacinfo
from .extension_galleries import (
    EXTENSIONS_MS_GALLERY, EXTENSIONS_OPENVSX_GALLERY,
    EXTENSIONS_OPENVSX_TRUSTED,
)

FEATURES_PATCH_PATH = DATA_DIR / "patch/features-patch.json"
TDKEY = "linkProtectionTrustedDomains"


def patch_features(product: dict[str, Any], config: dict[str, Any]):
    try:
        extra_features = config["extra_features"]
    except KeyError:
        return
    if not extra_features:
        return
    patch_data = json_load(FEATURES_PATCH_PATH)
    for key in patch_data.keys():
        product[key] = patch_data[key]


def patch_data_dir(product: dict[str, Any], config: dict[str, Any]):
    try:
        use_xdg = config["use_xdg"]
    except KeyError:
        return
    if not use_xdg:
        return
    product["dataFolderName"] = ".local/share/vscodium"


def patch_marketplace_trusted_domains(product: dict[str, Any]):
    cur_domains: list[str]
    try:
        cur_domains = product[TDKEY]
    except KeyError:
        cur_domains = []
    for domain in EXTENSIONS_OPENVSX_TRUSTED:
        with suppress(ValueError):
            cur_domains.remove(domain)
    if not cur_domains:
        with suppress(KeyError):
            product.pop(TDKEY)
    else:
        product[TDKEY] = cur_domains


def patch_marketplace(product: dict[str, Any], config: dict[str, Any]):
    try:
        marketplace = config["extensions_source"]
    except KeyError:
        return
    gallery = {}
    domains_remove = False
    match marketplace:
        case "openvsx":
            gallery = EXTENSIONS_OPENVSX_GALLERY
        case "microsoft":
            gallery = EXTENSIONS_MS_GALLERY
            domains_remove = True
        case _:
            pacinfo("Invalid marketplace:", marketplace)
            return
    if gallery:
        product["extensionsGallery"] = gallery
    if domains_remove:
        patch_marketplace_trusted_domains(product)


def patch_pkg(editor_path: Path, config: dict[str, Any]):
    patch_config: dict[str, Any] = config["patch"]
    product_path = editor_path / "resources/app/product.json"
    product = json_load(product_path)
    # Patch 1: Features
    patch_features(product, patch_config)
    # Patch 2: Data dir
    patch_data_dir(product, patch_config)
    # Patch 3: Marketplace
    patch_marketplace(product, patch_config)
    json_write(product_path, product, indent=2)


def patch_pkgs(packages: list[str]):
    config = get_config()
    conf_packages: dict[str, str] = config["packages"]
    changed_packages = [
        pkg
        for pkg in packages
        if pkg in conf_packages
    ]
    for pkg in changed_packages:
        pacinfo("Patching", pkg)
        patch_pkg(Path(conf_packages[pkg]), config)
