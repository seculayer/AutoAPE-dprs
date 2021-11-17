import logging
import re
import urllib.parse as decode
from typing import List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class SpecialCharExtract(AbstractConvert):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._max_len = int(self.arg_list[0])
        self.num_feat = self._max_len

    def apply(self, data: str) -> List:
        def to_float(x: str):
            try:
                return float(ord(x))
            except Exception as exc:
                logging.warning(exc)
                return 255.0

        # URL Decode
        try:
            data = data.replace("\\/", "/")
            decoded_data = decode.unquote(data)
        except Exception as e:
            logging.warning(e)
            decoded_data = data

        # replace special characters
        try:
            replaced_data = re.findall(r"[\W_]", decoded_data)
        except Exception as e:
            logging.warning(e)
            replaced_data = decoded_data

        result = list(map(lambda x: to_float(x), replaced_data[: self._max_len]))

        # padding
        if len(result) < self._max_len:
            result.extend([255.0] * (self._max_len - len(result)))

        return result
