import base64
import logging
from typing import List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class DecodeBase64(AbstractConvert):
    def apply(self, data: str) -> List[str]:
        char_set = "utf-8"

        if isinstance(data, str):
            if data.strip():
                data = data.encode(char_set)
            else:
                return [""]
        else:
            return [""]

        try:
            result = base64.b64decode(data)
            return [result.decode(char_set)]
        except Exception as e:
            logging.error(e)
            return [""]
