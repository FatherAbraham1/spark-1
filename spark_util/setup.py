#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import commands
from setuptools import setup, find_packages
from distutils.sysconfig import get_python_lib

setup_status = setup(
    name = "spark_util",
    version = "4.0",
    packages = find_packages(),
    package_data = {
        '': ['*.py']
    },
    data_files = [
        ('conf', ['conf/namenode.conf'])
    ],
    install_requires = [
    ],
    author = "chenguolin",
    author_email = "cgl1079743846@gmail.com",
    description = "This is an about Spark Python util package"
)

##############################################################################################################
try:
    os.system('rm -rf dist')
    os.system('rm -rf build')
    os.system('rm -rf *.egg-info')
except Exception,e:
    print "clean install info exception:[%s]" % str(e)
