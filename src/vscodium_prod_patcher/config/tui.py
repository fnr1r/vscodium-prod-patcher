import sys
from pathlib import Path
from typing import Any, Optional

from ..hooks.install import write_update_hook_cfg
from ..shared import eprint
from .schema import VscEditorConfig, VscEditorMetaConfig

try:
    import inquirer
except ImportError:
    # err is NoReturn, but vscode is being a
    eprint("TUI configuration requires python-inquirer")
    sys.exit(1)

from ..utils.friendlybool import (
    FRIENDLY_BOOL_STRS, friendly_bool_to_str_opt, friendly_str_to_bool,
)
from .main import get_config, save_config
from .utils import list_vscodium_packages, try_guess_editor_meta


def prompt_for_editor_meta_config(pkg: str) -> Optional[VscEditorMetaConfig]:
    print("Manually configure", pkg)
    print("Please input the editor path and relative product.json path")
    print(f"(for example /usr/lib/{pkg} and resources/app/product.json)")
    questions = [
        inquirer.Path("editor_path"),
        inquirer.Path("product_json_path"),
    ]
    while True:
        answers_maybe = inquirer.prompt(questions)
        if answers_maybe is None:
            return None
        assert isinstance(answers_maybe, dict)
        answers: dict[str, Any] = answers_maybe
        editor_path = Path(answers["editor_path"])
        product_json_path = Path(answers["product_json_path"])
        if not editor_path.exists():
            eprint("Editor path does not exist! Try again.")
            continue
        abs_product_json_path = editor_path / product_json_path
        if not (
            abs_product_json_path.exists()
            and abs_product_json_path.is_file()
        ):
            eprint("product.json does not exist! Try again.")
            continue
        break
    return VscEditorMetaConfig(editor_path, product_json_path)


def try_get_editor_meta(pkg: str) -> Optional[VscEditorMetaConfig]:
    meta = try_guess_editor_meta(pkg)
    if meta is not None:
        print("Found VSCodium editor info:", meta)
        return meta
    eprint("Editor metadata could not be autodetected.")
    return prompt_for_editor_meta_config(pkg)


def config_packages():
    vscodium_packages = list_vscodium_packages()
    if len(vscodium_packages) == 0:
        raise RuntimeError("VSCodium is not installed")
    config = get_config()
    packages = config.packages
    for package in packages:
        if package in vscodium_packages:
            continue
        print(f"{package} is not installed. Remove it from config?", end="")
        ans = input(" [y/N]: ")
        if len(ans) < 1 or ans[0].lower() != "y":
            continue
        packages.pop(package)
    for package_name in vscodium_packages:
        if package_name in packages:
            continue
        meta = try_get_editor_meta(package_name)
        if meta is None:
            print("Failed to get info on", package_name + ".", "Skipping.")
            continue
        editor_info = VscEditorConfig(meta)
        packages[package_name] = editor_info
    save_config(config)
    write_update_hook_cfg(config)


def config_features():
    config = get_config()
    features = config.patch
    questions = [
        inquirer.List(
            "extensions_source",
            "Select an extension marketplace / gallery",
            ["openvsx", "microsoft"],
            default=features.extension_source,
        ),
        inquirer.List(
            "extra_features",
            "Do you want to enable extra features that may be required by some"
            + " Micro$oft extensions?",
            FRIENDLY_BOOL_STRS,
            default=friendly_bool_to_str_opt(features.extra_features),
        ),
        inquirer.Text(
            "data_dir",
            "Which data directory do you want to use? Empty for default."
            + " (default is `.vscode-oss`)",
        ),
    ]
    answers_maybe = inquirer.prompt(questions)
    assert answers_maybe is not None
    answers: dict[str, Any] = answers_maybe
    extra_features = friendly_str_to_bool(answers["extra_features"])
    features.extension_source = answers["extensions_source"]
    features.extra_features = extra_features
    data_dir: str = answers["data_dir"]
    if not data_dir:
        features.data_dir = None
    else:
        features.data_dir = Path(data_dir)
    config.patch = features
    save_config(config)
