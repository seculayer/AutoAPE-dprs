from typing import List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class IPNormal(AbstractConvert):
    _max: int
    _min: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._max = 255
        self._min = 0
        self.num_feat = 4

    def apply(self, data: str) -> List[int]:
        default_result = [0.0, 0.0, 0.0, 0.0]

        if not isinstance(data, str):
            return default_result

        ip_split = data.split(".")
        if len(ip_split) != self.num_feat:
            return default_result

        norm = self._max - self._min

        try:
            result = list(map(lambda x: ((float(x) - self._min) / norm), ip_split))
        except Exception as e:
            logging.error(e)
            return default_result

        return result
