from subprocess import PIPE, run


def pacman_list_packages_cmd() -> list[str]:
    p = run(
        ["pacman", "-Qq"],
        stdout=PIPE,
        check=True,
    )
    return p.stdout.decode().split()[:-1]
