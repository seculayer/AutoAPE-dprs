import logging
from typing import List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class LongToIP(AbstractConvert):
    def apply(self, data: int) -> List[str]:
        try:
            # TODO: add validation input range
            return [".".join(str(data >> (i << 3) & 0xFF) for i in reversed(range(4)))]
        except Exception as e:
            logging.error(e)
            return ["0.0.0.0"]  # ?
