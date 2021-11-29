import logging
from typing import List, Sequence

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class EqpDtTokenizer(AbstractConvert):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.num_feat = 2

    def apply(self, data: Sequence) -> List[float]:
        try:
            return [float(data[8:10]), float(data[10:12])]
        except Exception as e:
            logging.error(e)
            return [99.0, 99.0]
