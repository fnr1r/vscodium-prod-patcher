from abc import ABC
from typing import Any, Callable, Type, TypeVar

from mashumaro.mixins.dict import DataClassDictMixin

from .de import alpm_ini_loads

T = TypeVar("T", bound="DataClassAlpmIniMixin")

EncodedData = str
Encoder = Callable[[Any], EncodedData]
Decoder = Callable[[EncodedData], dict[Any, Any]]


class DataClassAlpmIniMixin(DataClassDictMixin, ABC):
    __slots__ = ()

    # NOTE: Used by DataClassDictMixin
    # pylint: disable=unused-private-member
    __mashumaro_builder_params = {
        "packer": {},
        "unpacker": {
            "format_name": "alpm_ini",
            "decoder": alpm_ini_loads,
        },
    }

    # NOTE: toml has final, but is overriden by DataClassDictMixin
    @classmethod
    def from_alpm_ini(
        cls: Type[T],
        data: EncodedData,
        decoder: Decoder = alpm_ini_loads,
        **from_dict_kwargs: Any,
    ) -> T:
        raise NotImplementedError
