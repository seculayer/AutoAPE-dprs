import logging
from typing import List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class IPTransferDivide(AbstractConvert):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_feat = 4

    def apply(self, data: str) -> List[str]:
        try:
            return data.split(".")
        except Exception as e:
            logging.error(e)
            return ["0", "0", "0", "0"]
