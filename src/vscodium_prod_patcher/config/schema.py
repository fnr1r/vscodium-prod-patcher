from dataclasses import dataclass, field
from pathlib import Path

from mashumaro.mixins.toml import DataClassTOMLMixin


@dataclass
class VscPatchConfig:
    extensions_source: str = field(default="openvsx")
    extra_features: bool = field(default=False)
    use_xdg: bool = field(default=False)


@dataclass
class Config(DataClassTOMLMixin):
    packages: dict[str, Path] = field(default_factory=dict)
    patch: VscPatchConfig = field(default_factory=VscPatchConfig)
