import logging
from typing import List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class IPTransferMerge(AbstractConvert):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_feat = 1

    def apply(self, data: str) -> List[str]:
        try:
            data1, data2, *_ = data
            return [data1 + "." + data2] * 6
        except Exception as e:
            logging.error(e)
            return ["0", "0", "0", "0", "0", "0"]
