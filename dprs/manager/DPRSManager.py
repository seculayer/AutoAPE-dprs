# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.
import json
from typing import Dict

from dprs.common.info.DPRSJobInfo import DPRSJobInfo
from dprs.common.Constants import Constants
from dprs.common.Common import Common
from dprs.manager.SFTPClientManager import SFTPClientManager
from dprs.recommender.dp.RandomDataProcessor import RandomDataProcessor
from dprs.recommender.fs.RandomFeatureSelection import RandomFeatureSelection


class DPRSManager(object):
    # class : DataAnalyzerManager
    def __init__(self, job_id, job_idx):
        self.logger = Common.LOGGER.get_logger()

        self.mrms_sftp_manager: SFTPClientManager = SFTPClientManager(
            "{}:{}".format(Constants.MRMS_SVC, Constants.MRMS_SFTP_PORT), Constants.MRMS_USER, Constants.MRMS_PASSWD)

        self.job_info: Dict = self.load_job_info(job_id)
        self.dataset_meta: Dict = self.load_meta_info(self.job_info.get("data_anls_info").get("dataset_id"))

        self.logger.info("DPRSManager initialized.")

    def load_job_info(self, job_id):
        filename = "{}/RCMD_{}.job".format(Constants.DIR_DIVISION_PATH, job_id)
        print(filename)
        return self.mrms_sftp_manager.load_json_data(filename)

    def load_meta_info(self, dataset_id):
        filename = "{}/DA_META_{}.info".format(Constants.DIR_DIVISION_PATH, dataset_id)
        return self.mrms_sftp_manager.load_json_data(filename)

    def recommender(self):
        feature_selection = RandomFeatureSelection().recommend(self.dataset_meta.get("meta"))
        functions = RandomDataProcessor().recommend(feature_selection)

    def terminate(self):
        self.mrms_sftp_manager.close()


if __name__ == '__main__':
    dam = DPRSManager("ID", "0")
