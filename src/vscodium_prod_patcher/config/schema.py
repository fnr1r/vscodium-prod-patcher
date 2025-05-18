from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from mashumaro.mixins.toml import DataClassTOMLMixin


@dataclass
class VscPatchConfig:
    data_dir: Optional[Path] = field(default=None)
    extension_source: Optional[str] = field(default=None)
    extra_features: Optional[bool] = field(default=None)


@dataclass
class VscEditorMetaConfig:
    editor_path: Path
    product_json_path: Path


@dataclass
class VscEditorConfig:
    meta: VscEditorMetaConfig
    config_override: Optional[VscPatchConfig] = field(default=None)

    @property
    def editor_path(self) -> Path:
        return self.meta.editor_path

    @property
    def product_json_path(self) -> Path:
        meta = self.meta
        return meta.editor_path / meta.product_json_path


@dataclass
class Config(DataClassTOMLMixin):
    packages: dict[str, VscEditorConfig] = field(default_factory=dict)
    patch: VscPatchConfig = field(default_factory=VscPatchConfig)
