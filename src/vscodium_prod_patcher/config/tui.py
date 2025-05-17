import sys
from pathlib import Path
from typing import Any, Optional

from ..shared import eprint

try:
    import inquirer
except ImportError:
    # err is NoReturn, but vscode is being a
    eprint("TUI configuration requires python-inquirer")
    sys.exit(1)

from ..tui.friendlybool import (
    FRIENDLY_BOOL_STRS, friendly_bool_to_str, friendly_str_to_bool,
)
from .main import get_config, save_config
from .utils import list_vscodium_packages, try_guess_editor_path


def try_get_editor_path(pkg: str) -> Optional[Path]:
    path = try_guess_editor_path(pkg)
    if path is not None:
        print("Found VSCodium editor path:", path)
        return path
    answers_maybe = inquirer.prompt([inquirer.Path(
        "ans",
        f"The editor path for \"{pkg}\" could not be detected."
        + " Please enter it:",
    )])
    if answers_maybe is None:
        return None
    answer: str = answers_maybe["ans"]
    return Path(answer)


def config_packages():
    maybe_codiums = list_vscodium_packages()
    if len(maybe_codiums) == 0:
        raise RuntimeError("VSCodium is not installed")
    if len(maybe_codiums) == 1:
        pkg = maybe_codiums.pop()
        print("Assuming VSCodium package is", pkg)
    else:
        answers_maybe = inquirer.prompt([inquirer.List(
            "vscodiums",
            "Select VSCodium package you want to patch",
            maybe_codiums,
        )])
        assert answers_maybe is not None
        pkg = answers_maybe["vscodiums"]
    assert isinstance(pkg, str)
    packagesd: dict[str, Path] = {}
    app_path = try_guess_editor_path(pkg)
    if app_path is None:
        print("Skipping", pkg)
        return
    packagesd[pkg] = app_path
    config = get_config()
    config.packages = packagesd
    save_config(config)


def config_features():
    config = get_config()
    features = config.patch
    questions = [
        inquirer.List(
            "extra_features",
            "Do you want to enable extra features that may be required by some"
            + " Micro$oft extensions?",
            FRIENDLY_BOOL_STRS,
            default=friendly_bool_to_str(features.extra_features),
        ),
        inquirer.List(
            "extensions_source",
            "Select an extension marketplace / gallery",
            ["openvsx", "microsoft"],
            default=features.extensions_source,
        ),
        inquirer.List(
            "use_xdg",
            "Do you want to change the extension data directory to comply with"
            + " XDG?",
            FRIENDLY_BOOL_STRS,
            default=friendly_bool_to_str(features.use_xdg),
        ),
    ]
    answers_maybe = inquirer.prompt(questions)
    assert answers_maybe is not None
    answers: dict[str, Any] = answers_maybe
    extra_features = friendly_str_to_bool(answers["extra_features"])
    features.extra_features = extra_features
    features.extensions_source = answers["extensions_source"]
    features.use_xdg = friendly_str_to_bool(answers["use_xdg"])
    config.patch = features
    save_config(config)
