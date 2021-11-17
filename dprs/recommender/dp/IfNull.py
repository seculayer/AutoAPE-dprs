from typing import Any, List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class IfNull(AbstractConvert):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._replace = self.arg_list[0]

    def apply(self, data: Any) -> List:
        if data and isinstance(data, str) and data.strip():
            return [data]
        else:
            return [self._replace]
