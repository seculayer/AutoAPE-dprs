# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team
######################################################################################

from setuptools import setup, find_packages

from dprs.common.utils.FileUtils import FileUtils
from dprs.common.tools.VersionManagement import VersionManagement

######################################################################################
MODULE_NM = "dprs"
version_manager = VersionManagement(FileUtils.get_realpath(file=__file__)+"/"+MODULE_NM)


VERSION = version_manager.VERSION

print(version_manager.print_version())
print("building {}....".format(MODULE_NM))
######################################################################################
# required packages
f = open("requirements.txt", "r")
REQUIRED_PACKAGES = f.readlines()
f.close()
######################################################################################
print("-------------------------------------------------------------------------------")
print("--- Additional File list ---")
# Additional file list
FILE_LIST = [FileUtils.get_realpath(file=__file__)+"/"+MODULE_NM+"/VERSION"]
FILE_LIST += FileUtils.read_dir(
    directory=FileUtils.get_realpath(file=__file__) + "/dprs/resources/conf", ext=".xml"
)
FILE_LIST += FileUtils.read_dir(
    directory=FileUtils.get_realpath(file=__file__) + "/dprs/resources", ext=".json"
)
print(FILE_LIST)
print("-------------------------------------------------------------------------------")
######################################################################################
# build package list
packages = find_packages(
        exclude=[
            "build", "tests", "scripts", "dists"
        ],
    )
print("--- sub package list ---")
print(packages)
print("-------------------------------------------------------------------------------")
######################################################################################
# setup script
# wheel command
# python setup.py bdist_wheel

setup(
    name=MODULE_NM,
    version=VERSION,
    description="",
    author="Jin Kim",
    author_email="jinkim@seculayer.co.kr",
    packages=packages,
    package_dir={
        "conf": "conf",
        "resources": "resources"
    },
    python_requires='>3.5.2',
    package_data={
        MODULE_NM: FILE_LIST
    },
    install_requires=REQUIRED_PACKAGES,
    zip_safe=False,
)
######################################################################################
