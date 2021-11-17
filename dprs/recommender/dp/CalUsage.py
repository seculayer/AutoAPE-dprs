import logging
from typing import List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class CalUsage(AbstractConvert):
    def apply(self, data: float) -> List[float]:
        try:
            return [float(data) / 100]
        except Exception as e:
            logging.error(e)
            return [0.0]
