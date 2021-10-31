# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.
import random
from typing import List, Dict


class RandomFeatureSelection(object):
    @staticmethod
    def recommend(meta_list: List[Dict]):
        max_features = len(meta_list)

        return random.sample(meta_list, random.randint(1, max_features))


