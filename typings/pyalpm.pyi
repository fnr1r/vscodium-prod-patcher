"""
# my own stub for pyalpm

GPL-3 just like pyalpm and the rest of the project

don't expect this to be always up to date

I'm not responsible for any thermo-nuclear war
"""

from typing import Callable, Optional

from _typeshed import Incomplete

# signature check levels
SIG_DATABASE = 1024
SIG_DATABASE_MARGINAL_OK = 4096
SIG_DATABASE_OPTIONAL = 2048
SIG_DATABASE_UNKNOWN_OK = 8192

# package reasons
PKG_REASON_DEPEND = 1
PKG_REASON_EXPLICIT = 0

# signature check levels
SIG_PACKAGE = 1
SIG_PACKAGE_MARGINAL_OK = 4
SIG_PACKAGE_OPTIONAL = 2
SIG_PACKAGE_UNKNOWN_OK = 8

LOG_DEBUG = 4
LOG_ERROR = 1
LOG_FUNCTION = 8
LOG_WARNING = 2


def version() -> str: ...
def alpmversion() -> str: ...
def vercmp(version1: str, version2: str) -> int: ...


_GroupTupleT = tuple[str, list[Package]]


class DB:
    # read-only
    name: str
    servers: list[str]
    # read-only
    pkgcache: list[Package]
    # read-only
    grpcache: list[_GroupTupleT]

    def get_pkg(self, pkgname: str) -> Optional[Package]: ...
    def read_grp(self, grpname: str) -> Optional[list[_GroupTupleT]]: ...
    def search(self, *args: str) -> list[Package]: ...
    def update(self, force: bool) -> bool: ...


class Package:
    db: Database

    # description properties
    name: str
    version: str
    desc: str
    url: str
    arch: str
    licenses: list[str]
    groups: list[str]

    # package properties
    packager: str
    md5sum: Optional[str]
    sha256sum: Optional[str]
    base64_sig: Optional[str]
    filename: str
    base: str
    size: int
    isize: int
    reason: int
    builddate: int
    installdate: int
    files: list[tuple[str, int, int]]
    backup: list[str]

    # dependency information
    depends: list[str]
    optdepends: list[str]
    checkdepends: list[str]
    makedepends: list[str]
    conflicts: list[str]
    provides: list[str]
    replaces: list[str]

    has_scriptlet: bool
    download_size: int

    def compute_requiredby(self) -> list[str]: ...
    def compute_optionalfor(self) -> list[str]: ...


class Database:
    name: str
    servers: list
    pkgcache: list
    grpcache: list[tuple[str, Incomplete]]

    def get_pkg(self, name: str) -> Optional[Package]: ...
    def update(self, force: bool) -> bool: ...
    def search(self, query: str) -> list[Package]: ...
    def read_grp(self, group: str) -> Optional[list[_GroupTupleT]]: ...


class Transaction:
    ...


class Handle:
    arch: list[str]
    cachedirs: list[str]
    checkspace: int
    dbext: str
    dbpath: str
    dlcb: Optional[Callable[[str, int, int], None]]
    eventcb: Optional[Callable[[Incomplete, str, Incomplete], Incomplete]]
    fetchcb: Optional[Incomplete]
    gpgdir: str
    ignoregrps: list[str]
    ignorepkgs: list[str]
    lockfile: str
    logfile: str
    noextracts: list[Incomplete]
    noupgrades: list[Incomplete]
    progresscb: Optional[Incomplete]
    questioncb: Optional[Incomplete]
    root: str
    usesyslog: int

    def __init__(self, rootpath: str, dbpath: str): ...
    def get_localdb(self) -> DB: ...
    def get_syncdbs(self) -> list[DB]: ...
    def register_syncdb(self, name: str, flags: int) -> DB: ...
    def set_pkgreason(self, package: Package, reason: int): ...
    def add_cachedir(self, path: str): ...
    def add_ignoregrp(self, groupname: str): ...
    def add_ignorepkg(self, pkgname: str): ...
    def add_noextract(self, pkgname: str): ...
    def add_noupgrade(self, pkgname: str): ...
    def init_transaction(
        self,
        nodeps: bool,
        force: bool,
        nosave: bool,
        nodepversion: bool,
        cascade: bool,
        recurse: bool,
        dbonly: bool,
        alldeps: bool,
        downloadonly: bool,
        noscriptlet: bool,
        noconflicts: bool,
        needed: bool,
        allexplicit: bool,
        unneeded: bool,
        recurseall: bool,
        nolock: bool,
    ) -> Transaction: ...


class error(Exception):
    args: tuple[str, int, str]
