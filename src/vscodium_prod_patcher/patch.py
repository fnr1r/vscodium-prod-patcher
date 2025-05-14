from pathlib import Path
from typing import Any

from .extension_galleries import (
    EXTENSIONS_OPENVSX_GALLERY, EXTENSIONS_OPENVSX_TRUSTED,
    EXTENSIONS_MS_GALLERY,
)
from .shared import (
    DATA_DIR, json_load, pacinfo, json_write,
)


def patch_features(product: dict[str, Any], config: dict[str, Any]):
    try:
        extra_features = config["extra_features"]
    except KeyError:
        return
    if not extra_features:
        return
    patch_path = DATA_DIR / "features-patch.json"
    patch_data = json_load(patch_path)
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
    TDKEY = "linkProtectionTrustedDomains"
    cur_domains: list[str]
    try:
        cur_domains = product[TDKEY]
    except KeyError:
        cur_domains = []
    for domain in EXTENSIONS_OPENVSX_TRUSTED:
        try:
            cur_domains.remove(domain)
        except ValueError:
            pass
    if not cur_domains:
        try:
            product.pop(TDKEY)
        except KeyError:
            pass
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


def patch_pkg(pkg: str, editor_path: Path, config: dict[str, Any]):
    pacinfo("Patching", pkg)
    product_path = editor_path / "resources/app/product.json"
    product = json_load(product_path)
    # Patch 1: Features
    patch_features(product, config)
    # Patch 2: Data dir
    patch_data_dir(product, config)
    # Patch 3: Marketplace
    patch_marketplace(product, config)
    json_write(product_path, product, indent=2)
