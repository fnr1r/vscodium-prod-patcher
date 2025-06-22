import json
import os
import shutil
from pathlib import Path
from typing import Any, Optional

from ..config.main import get_config
from ..consts import ENCODING
from ..paths import BACKUPS_DIR


def backup_json_file(
    original: Path,
    target: Path,
    load_and_dump_json_files: bool,
    json_dump_kwargs: Optional[dict[str, Any]] = None,
):
    if json_dump_kwargs is None:
        json_dump_kwargs = {}

    shutil.copy2(original, target)
    if not load_and_dump_json_files:
        return

    target_dbg_base_name = target.name.removesuffix(".json")
    target_dbg_name = target_dbg_base_name + ".load_and_dump.json"
    target_dbg = target.parent / target_dbg_name
    with (
        open(original, "rt", encoding=ENCODING) as file_in,
        open(target_dbg, "wt", encoding=ENCODING) as file_out,
    ):
        json.dump(json.load(file_in), file_out, **json_dump_kwargs)


def backup_editor_data(pkg: str):
    config = get_config()
    load_and_dump_json_files = \
        config.debug is not None \
        and bool(config.debug.load_and_dump_json_files)
    editor_meta = config.packages[pkg].meta
    current_backup_dir = BACKUPS_DIR / pkg
    os.makedirs(current_backup_dir, exist_ok=True)
    backup_json_file(
        editor_meta.abs_product_json_path,
        current_backup_dir / "product.json",
        load_and_dump_json_files,
        json_dump_kwargs={"indent": 2},
    )


def restore_editor_data(pkg: str):
    config = get_config()
    editor_meta = config.packages[pkg].meta
    current_backup_dir = BACKUPS_DIR / pkg
    shutil.copy2(
        current_backup_dir / "product.json",
        editor_meta.abs_product_json_path,
    )
