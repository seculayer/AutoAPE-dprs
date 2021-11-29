import abc
from typing import Any, Dict, List


class AbstractConvert(abc.ABC):
    _num_feature: int
    stat_dict: Dict[str, Any]
    arg_list: List

    _max_len: int
    _padding_val: int

    def __init__(self, arg_list: List = None, stat_dict: Dict[str, Any] = None):
        self._num_feature = 1

        self.stat_dict = stat_dict
        self.arg_list = arg_list

        self._max_len = 50
        self._padding_val = 255

    @property
    def num_feat(self):
        return self._num_feature

    @num_feat.setter
    def num_feat(self, num_feature: int):
        if isinstance(num_feature, int) and num_feature > 0:
            self._num_feature = num_feature

    @abc.abstractmethod
    def apply(self, data: Any) -> List:
        raise NotImplementedError
