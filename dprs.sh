#!/bin/bash
######################################################################################
# eyeCloudAI 3.1 MLPS Run Script
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.
######################################################################################

APP_PATH=/eyeCloudAI/app/ape

DPRS_LIB_PATH=$APP_PATH/dprs/lib
####
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export CUDA_HOME=/usr/local/cuda
export PYTHONPATH=$DPRS_LIB_PATH

KEY=${1}
WORKER_IDX=${2}

/usr/local/bin/python3.7 -m mars.DataProcessRecommender ${KEY} ${WORKER_IDX}
