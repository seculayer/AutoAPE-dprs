# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.
import random
from typing import List, Dict


class RandomFeatureSelection(object):
    @staticmethod
    def recommend(meta_list: List[Dict], target_field: str):
        target = []
        none_target = []

        for idx, meta in enumerate(meta_list):
            if meta.get("field_nm") == target_field:
                target.append(meta)
            else:
                none_target.append(meta)

        max_features = len(none_target)
        selections = random.sample(none_target, random.randint(1, max_features))

        return target.extend(selections)


