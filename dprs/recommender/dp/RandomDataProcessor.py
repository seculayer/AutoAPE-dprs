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
        print(self.cvt_fn_info)

    def get_cvt_fn(self):
        self.http_client.request("GET", "/mrms/get_cvt_fn")
        response = self.http_client.getresponse()
        data = json.loads(response.read())
        response.close()
        return data

    def recommend(self, feature_list):
        for feature in feature_list:
            feature["cvt_fn"] = random.choice(self.cvt_fn_info)
        return feature_list
