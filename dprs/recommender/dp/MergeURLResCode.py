import logging
from typing import List

from dprs.recommender.dp.AbstractConvert import AbstractConvert


class MergeURLResCode(AbstractConvert):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.num_feat = 1
        self._input_type = self.arg_list[0]

    def apply(self, data: List[List[str]]) -> List:
        try:
            data0, d0_flag = None, "str"
            data1, d1_flag = None, "str"

            try:
                data0 = int(data[0])
                d0_flag = "int"
            except:
                data0 = data[0]

            try:
                data1 = int(data[1])
                d1_flag = "int"
            except:
                data1 = data[1]

            res_code, url = None, None

            if d1_flag == "int":
                url, res_code = data0, data1
            elif d0_flag == "int":
                res_code, url = data0, data1

            if self._input_type == 0:
                url_split_list = url.split(" ")
                url = url_split_list[1]

            url = url.strip().split("?")[0]

            return [str(res_code) + "|" + str(url)]
        except Exception as e:
            logging.error(e)
            return ["#PADDING#|#PADDING#"] * self.num_feat
