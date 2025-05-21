import os
import shutil

from ..config.main import get_config
from ..paths import BACKUPS_DIR


def backup_editor_data(pkg: str):
    config = get_config()
    editor_meta = config.packages[pkg].meta
    current_backup_dir = BACKUPS_DIR / pkg
    os.makedirs(current_backup_dir, exist_ok=True)
    shutil.copy2(
        editor_meta.abs_product_json_path,
        current_backup_dir / "product.json",
    )


def restore_editor_data(pkg: str):
    config = get_config()
    editor_meta = config.packages[pkg].meta
    current_backup_dir = BACKUPS_DIR / pkg
    shutil.copy2(
        current_backup_dir / "product.json",
        editor_meta.abs_product_json_path,
    )
