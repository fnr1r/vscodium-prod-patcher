import filecmp
import os
import shlex
import shutil
from contextlib import suppress
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
from typing import Optional

from ..shared import eprint
from .singleton import AbstractSingleton

ArgsT = list[str]

DEFAULT_EDITOR = ["vi"]
KNOWN_SESSION_TYPES = ["wayland", "x11"]


def editor_from_env_var(key: str) -> ArgsT:
    return shlex.split(os.environ[key])


def is_desktop() -> bool:
    return "XDG_SESSION_TYPE" in os.environ


def find_editors() -> list[ArgsT]:
    # default to vi
    editors = [DEFAULT_EDITOR]
    with suppress(KeyError):
        editors.append(editor_from_env_var("EDITOR"))
    if is_desktop():
        with suppress(KeyError):
            editors.append(editor_from_env_var("VISUAL"))
    editors.reverse()
    return editors


def root_copy(
    src: Path,
    dest: Path,
    cp_flags: Optional[list[str]] = None,
    cp_impl: str = "cp",
    sudo_impl: str = "sudo",
):
    if cp_flags is None:
        cp_flags = []
    run(
        [sudo_impl, cp_impl] + cp_flags + [src, dest],
        check=True,
    )


class EditorWrap(AbstractSingleton):
    editors: list[ArgsT]

    def __init__(self):
        self.editors = find_editors()

    def _pre_edit_check(self, file: Path) -> os.stat_result:
        # this asserts if file.exists()
        stat = file.stat()
        if not file.is_file():
            # this should throw an exception
            with file.open("rb") as _:
                pass
        return stat

    def _edit_file(self, file: Path):
        filestr = str(file)
        if not self.editors:
            raise ValueError("no editors detected")
        for editor in self.editors:
            try:
                run(
                    editor + [filestr],
                    check=True,
                )
            except FileNotFoundError as e:
                eprint(e)
            else:
                break
        else:
            raise RuntimeError("no detected editors work")

    def edit_file(self, file: Path) -> bool:
        stat = self._pre_edit_check(file)
        self._edit_file(file)
        new_stat = file.stat()
        return stat.st_mtime != new_stat.st_mtime \
            or stat.st_mtime_ns != new_stat.st_mtime_ns

    def _edit_file_as_root(self, file: Path):
        with TemporaryDirectory() as tmpdir:
            tmpdirp = Path(tmpdir)
            tmpfile = tmpdirp / file.name
            shutil.copy2(file, tmpfile)
            self._edit_file(tmpfile)
            if not filecmp.cmp(file, tmpfile):
                root_copy(tmpfile, file)

    def edit_file_as_root(self, file: Path) -> bool:
        stat = self._pre_edit_check(file)
        if os.getuid() == 0:
            self._edit_file(file)
        else:
            self._edit_file_as_root(file)
        new_stat = file.stat()
        return stat.st_mtime != new_stat.st_mtime \
            or stat.st_mtime_ns != new_stat.st_mtime_ns
