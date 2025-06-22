from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from mashumaro.mixins.toml import DataClassTOMLMixin


@dataclass
class VscDebugConfig:
    load_and_dump_json_files: Optional[bool] = field(default=None)


@dataclass
class VscPatchConfig:
    data_dir: Optional[Path] = field(default=None)
    extension_source: Optional[str] = field(default=None)
    extra_features: Optional[bool] = field(default=None)


@dataclass
class VscEditorMetaConfig:
    editor_path: Path
    product_json_path: Path

    @property
    def abs_product_json_path(self) -> Path:
        return self.editor_path / self.product_json_path


@dataclass
class VscEditorConfig:
    meta: VscEditorMetaConfig
    patch_override: Optional[VscPatchConfig] = field(default=None)


@dataclass
class Config(DataClassTOMLMixin):
    debug: Optional[VscDebugConfig] = field(default=None)
    packages: dict[str, VscEditorConfig] = field(default_factory=dict)
    patch: VscPatchConfig = field(default_factory=VscPatchConfig)
