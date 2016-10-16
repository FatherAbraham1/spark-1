#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import warnings
from pyhdfs import HdfsClient
#warnings.filterwarnings('ignore')

FORMAT = '[%(levelname)s] [%(asctime)s] [%(filename)s::%(funcName)s::%(lineno)d] [%(message)s]'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('hdfs_client')


client = HdfsClient(hosts='localhost:9000')
print(client.list_status('/'))
