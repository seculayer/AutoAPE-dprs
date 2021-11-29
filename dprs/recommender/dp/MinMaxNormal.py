import logging
from typing import Any, List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class MinMaxNormal(AbstractConvert):
    _min: float
    _max: float

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self._min = float(self.stat_dict["min"])
            self._max = float(self.stat_dict["max"])
        except Exception as e:
            logging.warning(e)
            self._min = 0
            self._max = 0

    def apply(self, data: Any) -> List:
        norm = self._max - self._min
        if norm == 0:
            norm = 1

        result = -1.0

        try:
            result = (float(data) - self._min) / norm
        except Exception as e:
            logging.error(
                "[MinMaxNormal] Convert error: self.min {}, self.max: {}, data",
                self._min,
                self._max,
                data,
            )
            logging.error(e)

        return [result]
