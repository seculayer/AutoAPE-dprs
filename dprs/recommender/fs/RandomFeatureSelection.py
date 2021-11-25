# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.
import random
from typing import List, Dict
from dprs.common.Common import Common


class RandomFeatureSelection(object):
    Logger = Common.LOGGER.get_logger()
    @staticmethod
    def recommend(meta_list: List[Dict], target_field: str):
        target = []
        none_target = []
        target_field_nm = []
        feature_field_nm = []

        for idx, meta in enumerate(meta_list):
            if meta.get("field_nm") == target_field:
                target.append(meta)
                target_field_nm.append(meta.get("field_nm"))
            else:
                none_target.append(meta)

        RandomFeatureSelection.Logger.info("target : {}".format(target_field_nm))

        max_features = len(none_target)
        selections = random.sample(none_target, random.randint(1, max_features))

        RandomFeatureSelection.Logger.info("max_feature : {}".format(max_features))
        for _meta in selections:
            feature_field_nm.append(_meta.get("field_nm"))
        RandomFeatureSelection.Logger.info("selection : {}".format(feature_field_nm))

        rst = target + selections
        RandomFeatureSelection.Logger.debug("rst : {}".format(rst))
        return rst


