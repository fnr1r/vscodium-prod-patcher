from pathlib import Path

from ..config import get_config
from ..patch import patch_pkg


def patch_main(args):
    editor_path: Path = args.editor_path
    config = get_config()
    patch_pkg(editor_path, config)
