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

        for idx, meta in enumerate(meta_list):
            if meta.get("field_nm") == target_field:
                target.append(meta)
            else:
                none_target.append(meta)
        RandomFeatureSelection.Logger.info("target : {}".format(target))
        RandomFeatureSelection.Logger.info("non_target : {}".format(none_target))

        max_features = len(none_target)
        selections = random.sample(none_target, random.randint(1, max_features))

        RandomFeatureSelection.Logger.info("max_feature : {}".format(max_features))
        RandomFeatureSelection.Logger.info("selection : {}".format(selections))

        rst = target + selections
        RandomFeatureSelection.Logger.info("rst : {}".format(rst))
        return rst


