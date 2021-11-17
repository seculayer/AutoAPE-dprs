from typing import List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class ToLowerCase(AbstractConvert):
    def apply(self, data: str) -> List[str]:
        if isinstance(data, str) and data.strip():
            return [data.lower()]

        return [""]
