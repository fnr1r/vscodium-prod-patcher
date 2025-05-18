from pathlib import Path

from ..config import get_config
from ..config.schema import VscEditorConfig, VscEditorMetaConfig
from ..config.utils import try_product_json_path_from_editor_path
from ..patch import patch_pkg
from ..shared import err


def patch_main(args):
    editor_path: Path = args.editor_path
    product_json_path = try_product_json_path_from_editor_path(editor_path)
    if product_json_path is None:
        err("Failed to detect product.json path")
        return
    meta = VscEditorMetaConfig(editor_path, product_json_path)
    editor_config = VscEditorConfig(meta)
    config = get_config()
    patch_pkg(editor_config, config)
