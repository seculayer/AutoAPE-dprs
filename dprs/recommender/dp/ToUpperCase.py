from typing import List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class ToUpperCase(AbstractConvert):
    def apply(self, data: str) -> List[str]:
        if isinstance(data, str) and data.strip():
            return [data.upper()]

        return [""]
