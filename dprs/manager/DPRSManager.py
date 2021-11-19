# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.
import http.client
import json
import random
from typing import Dict

from dprs.common.Common import Common
from dprs.common.Constants import Constants
from dprs.manager.SFTPClientManager import SFTPClientManager
from dprs.recommender.dp.RandomDataProcessor import RandomDataProcessor
from dprs.recommender.fs.RandomFeatureSelection import RandomFeatureSelection


class DPRSManager(object):
    # class : DataAnalyzerManager
    def __init__(self, job_id, job_idx):
        self.logger = Common.LOGGER.get_logger()

        self.mrms_sftp_manager: SFTPClientManager = SFTPClientManager(
            "{}:{}".format(Constants.MRMS_SVC, Constants.MRMS_SFTP_PORT), Constants.MRMS_USER, Constants.MRMS_PASSWD)

        self.http_client: http.client.HTTPConnection = http.client.HTTPConnection(
            Constants.MRMS_SVC, Constants.MRMS_REST_PORT)

        self.job_id = job_id
        self.job_info: Dict = self.load_job_info(job_id)
        self.dataset_meta: Dict = self.load_meta_info(self.job_info.get("data_anls_info").get("dataset_id"))

        self.current = 0
        self.logger.info("DPRSManager initialized.")

    def load_job_info(self, job_id):
        filename = "{}/RCMD_{}.job".format(Constants.DIR_DIVISION_PATH, job_id)
        print(filename)
        return self.mrms_sftp_manager.load_json_data(filename)

    def load_meta_info(self, dataset_id):
        filename = "{}/DA_META_{}.info".format(Constants.DIR_DIVISION_PATH, dataset_id)
        return self.mrms_sftp_manager.load_json_data(filename)

    def get_uuid(self):
        self.http_client.request("GET", "/mrms/get_uuid")
        response = self.http_client.getresponse()
        return response.read().decode("utf-8").replace("\n", "")

    def recommender(self, job_id):
        results = list()
        self.http_client.request("POST", "/mrms/get_target_field", body=json.dumps({"project_id": job_id}))
        response = self.http_client.getresponse()
        project_target_field = response.read().decode("utf-8").replace("\n", "").replace("\"", "")
        self.logger.info("project_target_field: {}".format(project_target_field))

        for i in range(random.randint(2, 4)):
            feature_selection = RandomFeatureSelection().recommend(self.dataset_meta.get("meta"), project_target_field)
            # target idx는 0
            functions = RandomDataProcessor().recommend(feature_selection)

            body_json = {
                "project_id": job_id,
                "data_analysis_id": self.job_info.get("data_analysis_id"),
                "dp_analysis_id": self.get_uuid(),
                "data_analysis_json": functions,
            }
            results.append(body_json)

        self.http_client.request("POST", "/mrms/insert_dp_anls_info", body=json.dumps(results))
        response = self.http_client.getresponse()
        self.logger.info("{} {} {}".format(response.status, response.reason, response.read()))

        f = self.mrms_sftp_manager.get_client().open(
            "{}/DPRS_{}_{}.info".format(Constants.DIR_DIVISION_PATH, self.job_info.get("project_id"), self.current),
            "w"
        )
        f.write(json.dumps(results, indent=2))
        f.close()

    def terminate(self):
        self.mrms_sftp_manager.close()

    def get_terminate(self) -> bool:
        self.http_client.request("GET", "/mrms/get_proj_sttus_cd?project_id={}".format(self.job_id))
        response = self.http_client.getresponse()
        status = response.read().decode("utf-8")
        if status == Constants.STATUS_PROJECT_COMPLETE or status == Constants.STATUS_PROJECT_ERROR:
            return True
        return False


if __name__ == '__main__':
    dam = DPRSManager("ID", "0")
