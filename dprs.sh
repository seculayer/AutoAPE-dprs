#!/bin/bash
######################################################################################
# eyeCloudAI 3.1 MLPS Run Script
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.
######################################################################################

APP_PATH=/eyeCloudAI/app/ape

export PYTHONPATH=$PYTHONPATH:$APP_PATH/dprs/lib:$APP_PATH/dprs
export PYTHONPATH=$PYTHONPATH:$APP_PATH/pycmmn/lib:$APP_PATH/pycmmn
export PYTHONPATH=$PYTHONPATH:$APP_PATH/dataconverter/lib:$APP_PATH/dataconverter

KEY=${1}
WORKER_IDX=${2}

/usr/local/bin/python3.7 -m dprs.DataProcessRecommender ${KEY} ${WORKER_IDX}
