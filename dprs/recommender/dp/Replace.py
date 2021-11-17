from typing import Any, List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class Replace(AbstractConvert):
    _applicable: bool
    _old: str
    _new: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._applicable = False

        if len(self.arg_list) >= 2:
            self._old = self.arg_list[0]
            self._new = self.arg_list[1]
            self._applicable = True

    def apply(self, data: Any) -> List[str]:
        if not self._applicable:
            return [""]

        if data and isinstance(data, str) and data.strip():
            return [data.replace(self._old, self._new)]
        else:
            return [""]
