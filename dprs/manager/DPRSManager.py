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
from pycmmn.sftp.SFTPClientManager import SFTPClientManager
from dprs.recommender.dp.RandomDataProcessor import RandomDataProcessor
from dprs.recommender.fs.RandomFeatureSelection import RandomFeatureSelection


class DPRSManager(object):
    # class : DataAnalyzerManager
    def __init__(self, job_id, job_idx):
        self.logger = Common.LOGGER.getLogger()

        self.mrms_sftp_manager = None

        self.rest_root_url = f"http://{Constants.MRMS_SVC}:{Constants.MRMS_REST_PORT}"

        self.job_id = job_id
        self.job_info = None
        self.dataset_meta = None

        self.current = 0

    def initialize(self):
        self.mrms_sftp_manager: SFTPClientManager = SFTPClientManager(
            "{}:{}".format(Constants.MRMS_SVC, Constants.MRMS_SFTP_PORT),
            Constants.MRMS_USER, Constants.MRMS_PASSWD, self.logger
        )

        self.job_info: Dict = self.load_job_info(self.job_id)
        self.dataset_meta: Dict = self.load_meta_info(self.job_info.get("data_anls_info").get("dataset_id"))

        self.logger.info("DPRSManager initialized.")

    def load_job_info(self, job_id):
        filename = f"{Constants.DIR_JOB_PATH}/{job_id}/RCMD_{job_id}.job"
        print(filename)
        return self.mrms_sftp_manager.load_json_data(filename)

    def load_meta_info(self, dataset_id):
        filename = f"{Constants.DIR_DA_PATH}/{dataset_id}/DA_META_{dataset_id}.info"
        return self.mrms_sftp_manager.load_json_data(filename)

    def get_uuid(self):
        response = rq.get(f"{self.rest_root_url}/mrms/get_uuid")
        self.logger.info(f"get uuid : {response.status_code} {response.reason} {response.text}")
        return response.text.replace("\n", "")

    def recommender(self, job_id):
        results = list()
        response = rq.post(f"{self.rest_root_url}/mrms/get_target_field", json={"project_id": job_id})
        target_field = response.text.replace("\n", "").replace("\"", "")
        project_purpose_cd = self.job_info.get("project_purpose_cd")
        project_tag_list = rq.get(f"{self.rest_root_url}/mrms/get_project_tag?project_id={job_id}").text.split(",")
        self.logger.info(f"project_tag_list: {project_tag_list}")
        self.logger.info(f"get target field: {response.status_code} {response.reason} {target_field}")

        for i in range(random.randint(Constants.RCMD_MIN_COUNT, Constants.RCMD_MAX_COUNT)):
            feature_selection = RandomFeatureSelection().recommend(
                self.dataset_meta.get("meta"), target_field, project_tag_list
            )
            # target idx는 0
            functions = RandomDataProcessor().recommend(feature_selection, project_purpose_cd, project_tag_list)
            for func in functions:
                self.logger.info(f"project_id: {job_id}, field_name: {func['name']}, Recommended: {func['functions']}")

            body_json = {
                "project_id": job_id,
                "project_purpose_cd": self.job_info.get("project_purpose_cd", None),
                "data_analysis_id": self.job_info.get("data_analysis_id"),
                "dp_analysis_id": self.get_uuid(),
                "data_analysis_json": functions,
            }
            results.append(body_json)

        response = rq.post(f"{self.rest_root_url}/mrms/insert_dp_anls_info", json=results)
        self.logger.info(f"insert dp anls info: {response.status_code} {response.reason} {response.text}")

        f = self.mrms_sftp_manager.get_client().open(
            f"{Constants.DIR_JOB_PATH}/{job_id}/DPRS_{self.job_info.get('project_id')}_{self.current}.info",
            "w"
        )
        f.write(json.dumps(results, indent=2))
        f.close()

    def update_project_status(self, status):
        status_json = {"status": status, "project_id": self.job_id}
        response = rq.post(f"{self.rest_root_url}/mrms/update_projects_status", json=status_json)
        self.logger.info(f"update project status: {response.status_code} {response.reason} {response.text}")

    def terminate(self):
        if self.mrms_sftp_manager is not None:
            self.mrms_sftp_manager.close()

    def get_terminate(self) -> bool:
        response = rq.get(f"{self.rest_root_url}/mrms/get_proj_sttus_cd?project_id={self.job_id}")
        status = response.text
        if status == Constants.STATUS_PROJECT_COMPLETE or status == Constants.STATUS_PROJECT_ERROR:
            return True
        return False


if __name__ == '__main__':
    dam = DPRSManager("ID", "0")
