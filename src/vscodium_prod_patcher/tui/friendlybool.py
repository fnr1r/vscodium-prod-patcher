FRIENDLY_BOOL_STRS = ["no", "yes"]


def friendly_bool_to_str(b: bool):
    if b:
        return "yes"
    else:
        return "no"


def friendly_str_to_bool(t: str):
    match t:
        case "yes":
            return True
        case "no":
            return False
        case _:
            raise ValueError
