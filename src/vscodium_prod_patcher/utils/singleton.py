from abc import ABC


# pylint: disable=too-few-public-methods
class AbstractSingleton(ABC):  # noqa: B024
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance
