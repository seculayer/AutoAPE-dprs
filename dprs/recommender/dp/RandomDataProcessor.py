# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.

import requests as rq
import json
import random

from dprs.common.Constants import Constants


class RandomDataProcessor(object):
    def __init__(self):
        self.rest_root_url = f"http://{Constants.MRMS_SVC}:{Constants.MRMS_REST_PORT}"
        self.cvt_fn_info = self.get_cvt_fn()
        self.COMMON_FN_LIST = ["SISpWC", "XSSpWC"]  # , "SpecialCharExtract"]
        self.NUMERIC_FN_LIST = ["NotNormal", "OneHotEncode", "ZScoreNormal", "PortNormal", "MinMaxNormal"]
        self.LABEL_FN_LIST = ["OneHotEncode"]
        self.IMAGE_FN_LIST = ["MinMaxNormal"]
        self.TIME_FN_LIST = ["TimeToSerial"]

    def get_cvt_fn(self):
        response = rq.get(f"{self.rest_root_url}/mrms/get_cvt_fn")
        data = json.loads(response.text)
        result_dict = dict()
        for fn in data:
            result_dict[fn.get("conv_func_cls")] = fn.get("conv_func_tag")
        return result_dict

    def recommend(self, feature_list, project_purpose_cd):
        result = list()

        for idx, feature in enumerate(feature_list):
            field = dict()
            field["name"] = feature.get("field_nm")
            field["field_sn"] = feature.get("field_idx")
            field["field_type"] = feature.get("field_type")

            if idx == 0:
                # Case Target
                if project_purpose_cd == "10":  # TA
                    class_nm = "NotNormal"
                else:
                    class_nm = random.choice(self.LABEL_FN_LIST)
            else:
                if feature.get("field_type") == "string":
                    class_nm = random.choice(self.COMMON_FN_LIST)
                elif feature.get("field_type") == "image":
                    class_nm = random.choice(self.IMAGE_FN_LIST)
                elif feature.get("field_type") == "date":
                    class_nm = random.choice(self.TIME_FN_LIST)
                else:
                    class_nm = random.choice(self.NUMERIC_FN_LIST)

            functions: str = self.cvt_fn_info[class_nm]
            # TODO : temp
            if class_nm == "SpecialCharExtract":
                param_idx = functions.find('(')
                functions = functions[: param_idx + 1] + '64' + functions[param_idx + 1:]
            elif class_nm == "SISpWC" or class_nm == "XSSpWC":
                param_idx = functions.find('(')
                functions = functions[: param_idx + 1] + '64,255' + functions[param_idx + 1:]

            field["functions"] = functions
            field["statistic"] = feature.get("statistics")
            result.append(field)
        return result


if __name__ == '__main__':
    RandomDataProcessor()

