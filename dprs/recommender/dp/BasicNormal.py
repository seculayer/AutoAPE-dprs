import logging
import string
from typing import Any, List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class BasicNormal(AbstractConvert):
    _max: int
    _min: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._max = 32767
        self._min = 0

    def apply(self, data: Any) -> List:
        result = ""
        norm = self._max - self._min

        if data is None:
            data = 0

        if isinstance(data, str) and data.isalpha():
            lower_text = data.lower()
            data = sum(map(lambda x: string.ascii_lowercase.find(x), lower_text))

        try:
            result = (float(data) - self._min) / norm
        except Exception as e:
            logging.error(e)

        return [result]
