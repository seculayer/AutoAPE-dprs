import logging
import re
from typing import Any, List, Pattern

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class RegexGet(AbstractConvert):
    _regex: Pattern

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._regex = re.compile(self.arg_list[0])

    def apply(self, data: Any) -> List[str]:
        if data is None:
            return [""]

        if isinstance(data, str) and not data.strip():
            return [""]

        if self._regex.groups == 0:
            return [""]

        result = ""

        try:
            match_ = self._regex.match(data)
            if match_:
                result = match_.groups()[0]
        except Exception as e:
            logging.error(e)

        return [result]
