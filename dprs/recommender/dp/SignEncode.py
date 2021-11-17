import logging
from typing import Any, List, Optional

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class SignEncode(AbstractConvert):
    _max: int
    _min: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._max = 1
        self._min = 0

    def apply(self, data: int) -> Optional[List[int]]:
        if data != self._min and data != self._max:
            logging.error("input value is invalid.")
            return None

        if data == 0:
            result = -1
        else:
            result = 1

        return [result]
