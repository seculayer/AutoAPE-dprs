# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.
import requests as rq
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

        self.rest_root_url = f"http://{Constants.MRMS_SVC}:{Constants.MRMS_REST_PORT}"

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
        response = rq.get(f"{self.rest_root_url}/mrms/get_uuid")
        self.logger.info(f"get uuid : {response.status_code} {response.reason} {response.text}")
        return response.text.replace("\n", "")

    def recommender(self, job_id):
        results = list()
        response = rq.post(f"{self.rest_root_url}/mrms/get_target_field", json={"project_id": job_id})
        project_target_field = response.text.replace("\n", "").replace("\"", "")
        self.logger.info(f"get target field: {response.status_code} {response.reason} {project_target_field}")

        for i in range(random.randint(Constants.RCMD_MIN_COUNT, Constants.RCMD_MAX_COUNT)):
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

        response = rq.post(f"{self.rest_root_url}/mrms/insert_dp_anls_info", json=results)
        self.logger.info(f"insert dp anls info: {response.status_code} {response.reason} {response.text}")

        f = self.mrms_sftp_manager.get_client().open(
            "{}/DPRS_{}_{}.info".format(Constants.DIR_DIVISION_PATH, self.job_info.get("project_id"), self.current),
            "w"
        )
        f.write(json.dumps(results, indent=2))
        f.close()

    def terminate(self):
        self.mrms_sftp_manager.close()

    def get_terminate(self) -> bool:
        response = rq.get(f"{self.rest_root_url}/mrms/get_proj_sttus_cd?project_id={self.job_id}")
        status = response.text
        if status == Constants.STATUS_PROJECT_COMPLETE or status == Constants.STATUS_PROJECT_ERROR:
            return True
        return False


if __name__ == '__main__':
    dam = DPRSManager("ID", "0")
