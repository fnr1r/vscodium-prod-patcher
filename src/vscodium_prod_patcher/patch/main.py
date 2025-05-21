from contextlib import suppress
from typing import Any

from ..config.main import get_config
from ..config.schema import Config, VscEditorConfig, VscPatchConfig
from ..config.utils import merge_patch_config
from ..paths import DATA_DIR
from ..shared import json_load, json_write, pacinfo
from .extension_galleries import (
    EXTENSIONS_MS_GALLERY, EXTENSIONS_OPENVSX_GALLERY,
    EXTENSIONS_OPENVSX_TRUSTED,
)

FEATURES_PATCH_PATH = DATA_DIR / "patch/features-patch.json"
TDKEY = "linkProtectionTrustedDomains"


def patch_features(product: dict[str, Any], config: VscPatchConfig):
    extra_features = config.extra_features
    if not extra_features:
        return
    patch_data = json_load(FEATURES_PATCH_PATH)
    for key in patch_data.keys():
        product[key] = patch_data[key]


def patch_data_dir(product: dict[str, Any], config: VscPatchConfig):
    data_dir = config.data_dir
    if not data_dir:
        return
    product["dataFolderName"] = str(data_dir)


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


def patch_marketplace(product: dict[str, Any], config: VscPatchConfig):
    marketplace = config.extension_source
    if marketplace is None:
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


def patch_pkg(editor: VscEditorConfig, config: Config):
    patch_config = merge_patch_config(config.patch, editor.config_override)
    product_path = editor.meta.abs_product_json_path
    product = json_load(product_path)

    patch_features(product, patch_config)
    patch_marketplace(product, patch_config)
    patch_data_dir(product, patch_config)

    json_write(product_path, product, indent=2)


def patch_pkgs(packages: list[str]):
    config = get_config()
    conf_packages = config.packages
    changed_packages = [
        pkg
        for pkg in packages
        if pkg in conf_packages
    ]
    for pkg in changed_packages:
        pacinfo("Patching", pkg)
        patch_pkg(conf_packages[pkg], config)
