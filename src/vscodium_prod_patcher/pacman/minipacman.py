from configparser import ConfigParser, NoOptionError
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

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
    config: ConfigParser
    _database_path: Optional[Path] = None
    _package_info: Optional[PackageInfoT] = None
    _package_files: dict[str, PacmanFiles]

    def __init__(self):
        self.config = ConfigParser(allow_no_value=True)
        self.config.read("/etc/pacman.conf")
        self._package_files = {}

    def get_db_path(self) -> Path:
        try:
            db_path = self.config.get("options", "DBPath")
        except NoOptionError:
            db_path = "/var/lib/pacman"
        return Path(db_path)

    @property
    def database_path(self) -> Path:
        if self._database_path is None:
            self._database_path = self.get_db_path()
        return self._database_path

    def get_package_info(self) -> PackageInfoT:
        local_db_path = self.database_path / "local"
        package_info = {}
        for filename in local_db_path.iterdir():
            if not filename.is_dir():
                continue
            pkg_desc = filename / "desc"
            with open(pkg_desc, "rt", encoding=ENCODING) as file:
                entry = PacmanDesc.from_alpm_ini(file.read())
            package_info[entry.name] = entry
        return package_info

    @property
    def package_info(self) -> PackageInfoT:
        if self._package_info is None:
            self._package_info = self.get_package_info()
        return self._package_info

    def get_package_files(self, name: str) -> PacmanFiles:
        package_info = self.package_info[name]
        package_version = package_info.version
        package_id = f"{name}-{package_version}"
        local_db_path = self.database_path / "local"
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
