from .command import pacman_list_packages_cmd
from .minipacman import MiniPacman


def pacman_list_packages() -> list[str]:
    packages = MiniPacman().list_packages()
    if not packages:
        packages = pacman_list_packages_cmd()
    return packages
