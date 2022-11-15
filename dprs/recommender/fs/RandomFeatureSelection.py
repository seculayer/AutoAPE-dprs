# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.
import random
from typing import List, Dict
from dprs.common.Common import Common


class RandomFeatureSelection(object):
    Logger = Common.LOGGER.getLogger()

    @staticmethod
    def recommend(meta_list: List[Dict], target_field: str, project_tag_list: List[str]):
        target = []
        none_target = []
        target_field_nm = []
        feature_field_nm = []
        is_specific_case = {
            "dga": ["query"],
            "packet": ["query", "rtt"],
            "meta": [
                "query",
                "not_before",
                "dns_recode_recode_ttl",
                "vt_whois_createDate@COMMA@vt_whois_expiryDate",
                "vt_whois_createDate@COMMA@vt_whois_updateDate",
                "dns_recode_type",
                "dns_recode_recode_ttl",
                "resolutions_count",
                "malicious",
                "popularity_ranks",
                "popularity_ranks",
                "popularity_ranks",
                "popularity_ranks",
                "popularity_ranks",
             ]
        }  # available value : "dga", "packet", meta

        for idx, meta in enumerate(meta_list):
            if meta.get("field_nm") == target_field:
                target.append(meta)
                target_field_nm.append(meta.get("field_nm"))
            else:
                none_target.append(meta)

        RandomFeatureSelection.Logger.info("target : {}".format(target_field_nm))
        max_features = len(none_target)
        RandomFeatureSelection.Logger.info("max_feature : {}".format(max_features))

        selections = list()
        field_list_to_find = list()
        for tag in project_tag_list:
            if "dga" in tag.lower():
                field_list_to_find = is_specific_case["dga"]
                break
            elif "packet" in tag.lower():
                field_list_to_find = is_specific_case["packet"]
                break
            elif "meta" in tag.lower():
                field_list_to_find = is_specific_case["meta"]
                break

        if len(field_list_to_find) > 0:
            for field_name in field_list_to_find:
                for field_meta in none_target:
                    if field_meta.get("field_nm") == field_name:
                        selections.append(field_meta)

        if len(selections) == 0:
            selections = random.sample(none_target, random.randint(1, max_features))

        RandomFeatureSelection.Logger.info("max_feature : {}".format(max_features))
        for _meta in selections:
            feature_field_nm.append(_meta.get("field_nm"))
        RandomFeatureSelection.Logger.info("selection : {}".format(feature_field_nm))

        rst = target + selections
        RandomFeatureSelection.Logger.debug("rst : {}".format(rst))
        return rst


