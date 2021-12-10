import time
from dprs.common.Singleton import Singleton
from dprs.common.thread.KubePodSafetyTermThread import KubePodSafetyTermThread
from dprs.common.Common import Common
from dprs.common.Constants import Constants
from dprs.manager.DPRSManager import DPRSManager


class DataProcessRecommender(KubePodSafetyTermThread, metaclass=Singleton):
    def __init__(self, job_id: str, job_idx: str):
        KubePodSafetyTermThread.__init__(self)
        self.logger = Common.LOGGER.get_logger()
        self.job_id = job_id

        self.dprs_manager = DPRSManager(job_id, job_idx)
        try:
            self.dprs_manager.initialize()
            self.logger.info("DataProcessRecommender Initialized!")
        except Exception as e:
            self.logger.error(e, exc_info=True)

    def run(self) -> None:
        try:
            self.dprs_manager.recommender(job_id=self.job_id)
        except Exception as e:
            self.logger.error(e, exc_info=True)
            self.dprs_manager.update_project_status(Constants.STATUS_PROJECT_ERROR)

        while not self.dprs_manager.get_terminate():
            time.sleep(10)

        self.logger.info("DataProcessRecommender terminate!")
        self.dprs_manager.terminate()


if __name__ == '__main__':
    import sys

    j_id = sys.argv[1]
    j_idx = sys.argv[2]

    dprs = DataProcessRecommender(j_id, j_idx)
    dprs.start()
    dprs.join()
