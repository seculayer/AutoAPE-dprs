import logging
from typing import Any, List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class ZScoreNormal(AbstractConvert):
    _mean: float
    _stddev: float

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self._mean = self.stat_dict["avg"]
            self._stddev = self.stat_dict["stddev"]
        except Exception as e:
            logging.error(e)
            self._mean = 0
            self._stddev = 1

    def apply(self, data: Any) -> List[int]:
        try:
            if self._stddev == 0:
                self._stddev = 1
                logging.warning("Standard Deviation value is zero. Set stddev to 1")

            result = (float(data) - float(self._mean)) / float(self._stddev)
        except Exception as e:
            logging.error(e)
            result = 0.0

        return [result]
