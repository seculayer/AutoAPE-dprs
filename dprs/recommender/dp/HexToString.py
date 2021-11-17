import binascii
import logging
from typing import Any, List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class HexToString(AbstractConvert):
    _char_set: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._char_set = self.arg_list[0]

    def apply(self, data: Any) -> List:
        if isinstance(data, str):
            if data.strip():
                data = data.encode(self._char_set)
            else:
                return [""]

        try:
            result = binascii.unhexlify(data)
            result = result.decode(self._char_set)
            return [result]
        except Exception as e:
            logging.error(e)
            return [""]
