import logging
from typing import Any, List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class PortNormal(AbstractConvert):
    _max: int
    _min: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._max = 65535
        self._min = 0

    def apply(self, data: Any) -> List:
        norm = self._max - self._min
        result = 0

        try:
            result = (float(data) - self._min) / norm
        except Exception as e:
            logging.error(e)

        return [result]
