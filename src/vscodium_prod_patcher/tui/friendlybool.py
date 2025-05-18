from typing import Optional

FRIENDLY_BOOL_STRS = ["no", "yes"]


def friendly_bool_to_str(b: bool) -> str:
    if b:
        return "yes"
    return "no"


def friendly_bool_to_str_opt(b: Optional[bool]) -> Optional[str]:
    if b is None:
        return None
    return friendly_bool_to_str(b)


def friendly_str_to_bool(t: str):
    match t:
        case "yes":
            return True
        case "no":
            return False
        case _:
            raise ValueError
