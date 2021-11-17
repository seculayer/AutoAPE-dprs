import logging
from typing import Any, List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class Substr(AbstractConvert):
    _applicable: bool
    _start_index: int
    _end_index: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._applicable = False
        if len(self.arg_list) >= 2:
            try:
                self._start_index = int(self.arg_list[0])
                self._end_index = int(self.arg_list[1])
                self._applicable = True
            except Exception as e:
                logging.error(e)

    def apply(self, data: Any) -> List[str]:
        if not self._applicable:
            return [""]

        if data and isinstance(data, str) and data.strip():
            if self._start_index > len(data):
                self._start_index = 0

            if self._end_index >= len(data):
                self._end_index = len(data)

            result = ""
            if self._end_index == 0:
                result = data[self._start_index :]
            else:
                result = data[self._start_index : self._end_index]

            return [result]
        else:
            return [""]
