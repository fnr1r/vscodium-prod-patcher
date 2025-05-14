import re
from typing import TextIO

KEY_RE = r"^%([A-Z]+)%$"


def package_desc_read(file: TextIO) -> dict[str, list[str]]:
    info = {}
    key = None
    value: list[str] = []
    for line in file.readlines():
        line = line[:-1]
        if key is None:
            m = re.match(KEY_RE, line)
            if m is None:
                continue
            key = m.group(1)
            continue
        if not line:
            info[key] = value
            key = None
            value = []
            continue
        value.append(line)
    return info
