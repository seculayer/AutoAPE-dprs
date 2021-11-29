from typing import Any, List, TypeVar

from dprs.recommender.dp.AbstractConvert import AbstractConvert

T = TypeVar("T", str, bytes, bytearray)


class Trim(AbstractConvert):
    def apply(self, data: Any) -> List[T]:
        if data and isinstance(data, (str, bytes, bytearray)) and data.strip():
            return [data.strip()]
        else:
            return [""]
