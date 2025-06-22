from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pyalpm import Handle
from pycman.config import PacmanConfig

from ..consts import ENCODING
from ..utils.singleton import AbstractSingleton
from .alpm_ini import DataClassAlpmIniMixin

PackageInfoT = dict[str, "PacmanDesc"]


@dataclass
class PacmanDesc(DataClassAlpmIniMixin):
    name: str
    version: str


@dataclass
class PacmanFiles(DataClassAlpmIniMixin):
    files: list[str]


class MiniPacman(AbstractSingleton):
    config: PacmanConfig
    _handle: Handle
    _database_path: Optional[Path] = None
    _package_info: Optional[PackageInfoT] = None
    _package_files: dict[str, PacmanFiles]

    def __init__(self, config_path: Optional[Path] = None):
        self.config = PacmanConfig(conf=config_path)
        self._package_files = {}

    @property
    def handle(self) -> Handle:
        if self._handle is None:
            self._handle = self.config.initialize_alpm()
        return self._handle

    def get_package_info(self) -> PackageInfoT:
        res: PackageInfoT = {}
        for pkg in self.handle.get_localdb().pkgcache:
            res[pkg.name] = PacmanDesc(pkg.name, pkg.version)
        return res

    @property
    def package_info(self) -> PackageInfoT:
        if self._package_info is None:
            self._package_info = self.get_package_info()
        return self._package_info

    def get_package_files(self, name: str) -> PacmanFiles:
        package_info = self.package_info[name]
        package_version = package_info.version
        package_id = f"{name}-{package_version}"
        db_path = Path(self.config.options["DBPath"])
        local_db_path = db_path / "local"
        files_info_path = local_db_path / package_id / "files"
        with open(files_info_path, "rt", encoding=ENCODING) as file:
            files_info = PacmanFiles.from_alpm_ini(file.read())
        return files_info

    def package_files(self, name: str) -> list[str]:
        res = self._package_files.get(name)
        if res is None:
            res = self.get_package_files(name)
            self._package_files[name] = res
        return res.files

    def list_packages(self) -> list[str]:
        return list(self.package_info.keys())
