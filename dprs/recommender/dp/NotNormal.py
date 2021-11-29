import logging
from typing import Any, List, Union

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class NotNormal(AbstractConvert):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_feat = 1

    def apply(self, data: Any) -> List[Union[float, str]]:
        result = ""

        try:
            if isinstance(data, int):
                result = float(data)
            elif isinstance(data, float):
                result = data
            elif isinstance(data, str):
                # Convert CRLF -> #CRLF#
                result = data.replace("[\r\n]+", "#CRLF#").replace("\\,", "#COMMA#")
        except Exception as e:
            logging.info(e)

        return [result]
