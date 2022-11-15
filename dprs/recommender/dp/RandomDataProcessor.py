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
        self.COMMON_FN_LIST = [["SISpWC", ["64", "255"]], ["XSSpWC", ["64", "255"]]]  # , "SpecialCharExtract"]
        self.NUMERIC_FN_LIST = [["NotNormal", []], ["OneHotEncode", []],
                                ["ZScoreNormal", []], ["PortNormal", []],
                                ["MinMaxNormal", []]]
        self.LABEL_FN_LIST = [["OneHotEncode", []]]
        self.IMAGE_FN_LIST = [["MinMaxNormal", []]]
        self.TIME_FN_LIST = [["TimeToSerial", []]]

        # META
        self.META_LIST = [
            [1, "query", ["DNSMetaPreProcessing",[]]],
            [2, "not_before", ["DateRemaining",[]]],
            [3, "dns_recode_recode_ttl", ["ListStddev",[]]],
            [4, "vt_whois_createDate@COMMA@vt_whois_expiryDate", ["DateDiff", []]],
            [5, "vt_whois_createDate@COMMA@vt_whois_updateDate", ["DateDiff", []]],
            [6, "dns_recode_type", ["ListUniqueType", []]],
            [7, "dns_recode_recode_ttl", ["ListLength", []]],
            [8, "resolutions_count", ["ListFirstValue", []]],
            [9, "malicious", ["VTMalicious", []]],
            [10, "popularity_ranks", ["VTPopularityRank", ["majestic"]]],
            [11, "popularity_ranks", ["VTPopularityRank", ["cisco"]]],
            [12, "popularity_ranks", ["VTPopularityRank", ["statvoo"]]],
            [13, "popularity_ranks", ["VTPopularityRank", ["alexa"]]],
            [14, "popularity_ranks", ["VTPopularityRank", ["quantcast"]]],
        ]

    def get_cvt_fn(self):
        response = rq.get(f"{self.rest_root_url}/mrms/get_cvt_fn")
        data = json.loads(response.text)
        result_dict = dict()
        for fn in data:
            result_dict[fn.get("conv_func_cls")] = fn.get("conv_func_tag")
        return result_dict

    def _function_recommend(self, idx, project_purpose_cd, field_nm, field_type, project_tag):
        class_nm_set = self._func_class_nm_random(field_type)

        if idx == 0:
            # Case Target
            if project_purpose_cd == "1":  # classification
                class_nm_set = random.choice(self.LABEL_FN_LIST)
            elif project_purpose_cd == "10":   # TA
                class_nm_set = ["NotNormal", []]
        else:
            if "dga" in project_tag:
                class_nm_set = self._func_class_nm_dga(field_nm, field_type)
            elif "packet" in project_tag:
                class_nm_set = self._func_class_nm_dns_packet(field_nm, field_type)

        return self._append_arg_list(class_nm_set)

    def _func_class_nm_random(self, field_type):
        if field_type == "string":
            random.choice(self.COMMON_FN_LIST)
        elif field_type == "image":
            return random.choice(self.IMAGE_FN_LIST)
        elif field_type == "date":
            return random.choice(self.TIME_FN_LIST)
        else:
            return random.choice(self.NUMERIC_FN_LIST)

    def _func_class_nm_dga(self, field_nm, field_type):
        if field_nm == "query":
            return ["DGAChar2IDX", []]
        else:
            return self._func_class_nm_random(field_type)

    def _func_class_nm_dns_packet(self, field_nm, field_type):
        if field_nm == "query":
            return ["DNSDomainPreProcessing", []]
        elif field_type == "rtt":
            return ["ZScoreNormal", []]
        else:
            return self._func_class_nm_random(field_type)

    def _func_class_nm_dns_meta(self, idx, field_nm, field_type):
        if idx == self.META_LIST[idx][0] and field_nm == self.META_LIST[idx][1]:
            return self.META_LIST[idx][2]
        else:
            return self._func_class_nm_random(field_type)

    def _append_arg_list(self, class_nm_set):
        functions = self.cvt_fn_info[class_nm_set[0]]
        arg_list = class_nm_set[1]
        if len(arg_list) != 0:
            param_idx = functions.find('(')
            return functions[: param_idx + 1] + ",".join(arg_list) + functions[param_idx + 1:]
        return functions

    def recommend(self, feature_list, project_purpose_cd, project_tag_list):
        project_tag = None
        for tag in project_tag_list:
            if "dga" in tag.lower():
                project_tag = "dga"
            elif "packet" in tag.lower():
                project_tag = "packet"
            elif "meta" in tag.lower():
                project_tag = "meta"

        result = list()
        for idx, feature in enumerate(feature_list):
            field = dict()
            field["name"] = feature.get("field_nm")
            field["field_sn"] = feature.get("field_idx")
            field["field_type"] = feature.get("field_type")
            field["functions"] = self._function_recommend(
                idx, project_purpose_cd, feature.get("field_nm"),
                feature.get("field_type"), project_tag)
            field["statistic"] = feature.get("statistics", {})
            result.append(field)
        return result


if __name__ == '__main__':
    RandomDataProcessor()
