from configparser import ConfigParser, NoOptionError
from pathlib import Path
from typing import Optional

from ..consts import ENCODING
from .pkgdesc import package_desc_read

PackageInfoT = dict[str, dict[str, list[str]]]


class MiniPacman:
    config: ConfigParser
    _database_path: Optional[Path] = None
    _package_info: Optional[PackageInfoT] = None

    def __init__(self):
        self.config = ConfigParser(allow_no_value=True)
        self.config.read("/etc/pacman.conf")

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
                entry = package_desc_read(file)
            pkg_name = entry["NAME"][0]
            package_info[pkg_name] = entry
        return package_info

    @property
    def package_info(self) -> PackageInfoT:
        if self._package_info is None:
            self._package_info = self.get_package_info()
        return self._package_info

    def list_packages(self) -> list[str]:
        return list(self.package_info.keys())
