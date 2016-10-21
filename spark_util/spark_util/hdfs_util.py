#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import warnings
from py_util import config_parse
from snakebite.client import HAClient
from snakebite.namenode import Namenode
#warnings.filterwarnings('ignore')

FORMAT = '[%(levelname)s] [%(asctime)s] [%(filename)s::%(funcName)s::%(lineno)d] [%(message)s]'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('hdfs_util')

def __create_hdfs_client__():
    try:
        namenode_conf = os.path.dirname(os.path.abspath(__file__)) + '/../conf/namenode.conf'
        config_dict = config_parse.config_parse(namenode_conf)
        if 'namenode' not in config_dict or 'host' not in config_dict['namenode'] or \
                'port' not in config_dict['namenode'] or 'second_namenode' not in config_dict or \
                'host' not in config_dict['second_namenode'] or 'port' not in config_dict['second_namenode']:
            logger.error('namenode config file:[%s] invalid\n' % namenode_conf)
            sys.exit(2)
        namenode_host = config_dict['namenode']['host']
        namenode_port = int(config_dict['namenode']['port'])
        second_namenode_host = config_dict['second_namenode']['host']
        second_namenode_port = int(config_dict['second_namenode']['port'])

        namenode = Namenode(namenode_host, namenode_port)
        second_namenode = Namenode(second_namenode_host, second_namenode_port)
        return HAClient([namenode, second_namenode], use_trash=True)
    except Exception,e:
        logger.error('create hdfs client exception:[%s]\n' % str(e))
        sys.exit(2)

hdfs_client = __create_hdfs_client__()

def cat(hdfs_file):
    """
    Cat HDFS file

    Parameters:
        @hdfs_file -- HDFS file, such as /user/hadoop/examples/data_0.dat
                      when hdfs_file is a directory, cause exception

    Returns:
        string content
        exception return None
    """
    try:
        gen = hdfs_client.cat([hdfs_file])
        return gen.next().next()
    except Exception,e:
        logger.error('cat file:[%s] exception:[%s]\n' % (hdfs_file, str(e)))
        return None

def copy_to_local(hdfs_file_list, local_path):
    """
    Copy HDFS files to local file system, HDFS Source is kept.
    When copying multiple, files, the destination must be a directory.

    Parameters:
        @hdfs_file_list -– HDFS files, such as ['/user/hadoop/examples/data_0.dat', '/user/hadoop/examples/data_1.dat']
        @local_path –- Local file or directory

    Returns:
        return True/False
    """
    try:
        gen = hdfs_client.copyToLocal(hdfs_file_list, local_path)
        for item in gen:
            print item
        return True
    except Exception,e:
        logger.error('copy hdfs file list to local exception:[%s]\n' % str(e))
        return False

print copy_to_local(['/user/hadoop/examples/data_0.dat', '/user/hadoop/examples/data_1.dat'], '/tmp/examples')
