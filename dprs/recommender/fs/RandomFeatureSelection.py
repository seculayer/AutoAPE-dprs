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
                "vtdlast_https_certificate_not_after",
                "vtdlast_dns_records_TTL",
                "vtdwhois_create_date@COMMA@vtdwhois_expiry_date",
                "vtdwhois_create_date@COMMA@vtdwhois_expiry_date",
                "vtdlast_dns_records_type",
                "vtdlast_dns_records_TTL",
                "vtdresolutions_count",
                "vtdlast_analysis_stats",
                "vtdpopularity",
                "vtdpopularity",
                "vtdpopularity",
                "vtdpopularity",
                "vtdpopularity",
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
            meta_idx = len(meta_list)
            for field_name in field_list_to_find:
                is_existed = False
                for field_meta in none_target:
                    if field_meta.get("field_nm").lower() == field_name:
                        selections.append(field_meta)
                        is_existed = True
                if not is_existed:
                    tmp_meta = {
                        "field_nm": field_name,
                        "field_idx": meta_idx,
                        "field_type": "null",
                        "type_stat": {},
                        "statistics": {
                            "basic": {
                                "min": 0,
                                "max": 0,
                                "mean": 0
                            }
                        },
                        "field_tag": []
                    }
                    meta_idx += 1
                    selections.append(tmp_meta)

        if len(selections) == 0:
            selections = random.sample(none_target, random.randint(1, max_features))

        RandomFeatureSelection.Logger.info("max_feature : {}".format(max_features))
        for _meta in selections:
            feature_field_nm.append(_meta.get("field_nm"))
        RandomFeatureSelection.Logger.info("selection : {}".format(feature_field_nm))

        rst = target + selections
        RandomFeatureSelection.Logger.debug("rst : {}".format(rst))
        return rst


