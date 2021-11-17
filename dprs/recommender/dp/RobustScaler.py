import logging
from typing import Any, List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class RobustScaler(AbstractConvert):
    _median: float
    _quantile_1: float
    _quantile_3: float
    _iqr: float

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self._median = float(self.stat_dict["median"])
            self._quantile_1 = float(self.stat_dict["quantile_1"])
            self._quantile_3 = float(self.stat_dict["quantile_3"])
        except Exception as e:
            logging.warning(e)
            self._median = 0
            self._quantile_1 = 0
            self._quantile_3 = 0

        self._iqr = self._quantile_3 - self._quantile_1

    def apply(self, data: Any) -> List[float]:
        result = 0.0

        try:
            if self._iqr == 0:
                self._iqr = 1
                logging.warning("IQR value was zero. It is not valid.")

            result = (float(data) - float(self._median)) / float(self._iqr)
        except Exception as e:
            logging.error(e)
            result = 0.0

        return [result]
