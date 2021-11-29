import re
from typing import Any, List, Pattern

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class ReplaceAll(AbstractConvert):
    _applicable: bool
    _regex: Pattern
    _new: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._applicable = False

        if len(self.arg_list) >= 2:
            self._regex = self.arg_list[0]
            self._new = self.arg_list[1]
            self._applicable = True

    def apply(self, data: Any) -> List[str]:
        if not self._applicable:
            return [""]

        if data and isinstance(data, str) and data.strip():
            return [re.sub(self._regex, self._new, data)]
        else:
            return [""]
