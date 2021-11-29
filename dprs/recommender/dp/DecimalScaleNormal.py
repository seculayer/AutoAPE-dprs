import logging
import math
from typing import List, Union

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class DecimalScaleNormal(AbstractConvert):
    _max: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._max = 32767

    def apply(self, data: Union[str, float, int]) -> List[float]:
        result = 0.0
        length = math.modf(math.log10(self._max) + 1)[1]

        try:
            result = float(data) / math.pow(10, length)
        except Exception as e:
            logging.error(e)

        return [result]
