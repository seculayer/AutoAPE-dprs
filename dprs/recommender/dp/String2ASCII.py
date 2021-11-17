import logging
from typing import List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class String2ASCII(AbstractConvert):
    _seq_len: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._max_len = int(self.arg_list[0])
        self._seq_len = int(self.arg_list[1])
        self.num_feat = self._max_len

    def apply(self, data: List[str]) -> List[List[int]]:
        try:
            if self._seq_len >= 0:
                features = [_to_ascii(x, self._max_len) for x in data[: self._seq_len]]
                if len(features) < self._seq_len:
                    features.extend(
                        [[0] * self._max_len] * (self._seq_len - len(features))
                    )
                return features
            else:
                return [[0] * self._max_len] * self._seq_len
        except Exception as e:
            logging.error(e, exc_info=True)
            return [[0] * self._max_len] * self._seq_len


def _to_ascii(str_: str, length: int) -> List[int]:
    if length >= 0:
        ord_seq = [ord(c) for c in str_[:length]]

        if len(ord_seq) < length:
            ord_seq.extend([0] * (length - len(ord_seq)))
        return ord_seq
    else:
        return [0] * length
