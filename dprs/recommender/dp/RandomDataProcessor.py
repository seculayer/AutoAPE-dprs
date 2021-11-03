# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.
import http.client
import json
import random

from dprs.common.Constants import Constants


class RandomDataProcessor(object):
    def __init__(self):
        self.http_client: http.client.HTTPConnection = http.client.HTTPConnection(
            Constants.MRMS_SVC, Constants.MRMS_REST_PORT)
        self.cvt_fn_info = self.get_cvt_fn()
        self.COMMON_FN_LIST = ["OneHotEncode"]
        self.NUMERIC_FN_LIST = ["NotNormal", "OneHotEncode", "ZScroeNormal", "PortNormal", "MinMaxNormal"]
        self.LABEL_FN_LIST = ["OneHotEncode"]

    def get_cvt_fn(self):
        self.http_client.request("GET", "/mrms/get_cvt_fn")
        response = self.http_client.getresponse()
        data = json.loads(response.read())
        response.close()
        result_dict = dict()
        for fn in data:
            result_dict[fn.get("conv_func_cls")] = fn.get("conv_func_tag")
        return result_dict

    def recommend(self, feature_list):
        result = list()

        for idx, feature in enumerate(feature_list):
            field = dict()
            field["name"] = feature.get("field_nm")
            field["field_sn"] = feature.get("field_idx")
            if feature.get("field_type") == "string":
                if idx == 0:
                    # Case Target
                    class_nm = random.choice(self.LABEL_FN_LIST)
                else:
                    class_nm = random.choice(self.COMMON_FN_LIST)
            else:
                if idx == 0:
                    # Case Target
                    class_nm = random.choice(self.LABEL_FN_LIST)
                else:
                    class_nm = random.choice(self.NUMERIC_FN_LIST)
            field["functions"] = self.cvt_fn_info[class_nm]
            field["statistic"] = {
                feature.get("field_nm"): field.get("statistics")
            }
            result.append(field)
        return result


if __name__ == '__main__':
    RandomDataProcessor()

