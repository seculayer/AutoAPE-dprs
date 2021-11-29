import hashlib
import logging
from typing import List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class StringToMD5(AbstractConvert):
    def apply(self, data: str) -> List[str]:
        if isinstance(data, str) and not data.strip():
            return [""]

        try:
            h = hashlib.md5()
            h.update(data.encode("utf-8"))
            return [h.hexdigest()]
        except Exception as e:
            logging.error(e)
            return [""]
