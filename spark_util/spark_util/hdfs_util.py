#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import warnings
from py_util import config_parse
from py_util import file_util
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
            logger.error('namenode config file:[%s] invalid' % namenode_conf)
            sys.exit(2)
        namenode_host = config_dict['namenode']['host']
        namenode_port = int(config_dict['namenode']['port'])
        second_namenode_host = config_dict['second_namenode']['host']
        second_namenode_port = int(config_dict['second_namenode']['port'])

        namenode = Namenode(namenode_host, namenode_port)
        second_namenode = Namenode(second_namenode_host, second_namenode_port)
        return HAClient([namenode, second_namenode], use_trash=True)
    except Exception,e:
        logger.error('create hdfs client exception:[%s]' % str(e))
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
        if hdfs_file == '' or hdfs_file is None:
            logger.error('parameter hdfs_file is empty')
            return None
        gen = hdfs_client.cat([hdfs_file])
        return gen.next().next()
    except Exception,e:
        logger.error('cat file:[%s] exception:[%s]' % (hdfs_file, str(e)))
        return None

def read(hdfs_file):
    """
    Read HDFS file

    Parameters:
        @hdfs_file -- HDFS file, such as /user/hadoop/examples/data_0.dat
                      when hdfs_file is a directory, cause exception

    Returns:
        string content
        exception return None
    """
    try:
        if hdfs_file == '' or hdfs_file is None:
            logger.error('parameter hdfs_file is empty')
            return None
        gen = hdfs_client.cat([hdfs_file])
        return gen.next().next()
    except Exception,e:
        logger.error('cat file:[%s] exception:[%s]' % (hdfs_file, str(e)))
        return None

def copy_to_local(hdfs_file_list, local_path):
    """
    Copy HDFS files to local file system, HDFS Source is kept.
    When copying multiple, files, the destination must be a directory.

    Parameters:
        @hdfs_file_list -– HDFS files, such as ['/user/hadoop/examples/data_0.dat', '/user/hadoop/examples/data_1.dat']
        @local_path –- Support normal file or directory

    Returns:
        return True/False
    """
    try:
        if hdfs_file_list is None or len(hdfs_file_list) == 0:
            logger.error('parameter hdfs_file_list is empty')
            return False
        if local_path == '' or local_path is None:
            logger.error('parameter local_path is empty')
            return False
        # mkdir parent dir
        parent_dir = local_path
        if len(hdfs_file_list) == 1:
            if local_path.rfind('/') >= 0:
                parent_dir = local_path[:local_path.rfind('/')]
            else:
                parent_dir = None
        if parent_dir is not None and file_util.exists(parent_dir) is False \
                and file_util.make_dir(parent_dir) is False:
            logger.error('make dir:[%s] fail' % parent_dir)
            return False
        # copy
        gen = hdfs_client.copyToLocal(hdfs_file_list, local_path)
        for item in gen:
            if item['result'] is False:
                logger.error('copy hdfs file:[%s] local error:[%s]' % (item['path'], item['error']))
                return False
        return True
    except Exception,e:
        logger.error('copy hdfs file list to local exception:[%s]' % str(e))
        return False

def count(hdfs_path):
    """
    Count all directorys and files in a hdfs path
    when hdfs_path is file return fileCount is 1

    Parameters:
        @hdfs_path –- HDFS path to count

    Returns:
        return dict contain key "directoryCount" and "fileCount"
        when exception return None
    """
    try:
        if hdfs_path == '' or hdfs_path is None:
            logger.error('parameter hdfs_path is empty')
            return None
        gen = hdfs_client.count([hdfs_path])
        res_dict = gen.next()
        return {
            'directoryCount': res_dict['directoryCount'],
            'fileCount': res_dict['fileCount']
        }
    except Exception,e:
        logger.error('count hdfs path:[%s] exception:[%s]' % (hdfs_path, str(e)))
        return None

def rm(hdfs_file):
    """
    Delete hdfs file

    Parameters:
        @hdfs_file –- HDFS file path

    Returns:
        return True/False
    """
    try:
        if hdfs_file == '' or hdfs_file is None:
            logger.error('parameter hdfs_file is empty')
            return False
        gen = hdfs_client.delete([hdfs_file])
        res_dict = gen.next()
        if res_dict['result'] == False:
            logger.error('remove hdfs file:[%s] error:[%s]' % (hdfs_file, res_dict['error']))
            return False
        return True
    except Exception,e:
        logger.error('remove hdfs file:[%s] exception:[%s]' % (hdfs_file, str(e)))
        return False

def ls(hdfs_path):
    """
    List hdfs path support directory and file

    Parameters:
        @hdfs_path –- HDFS path

    Returns:
        return dict contain key "directoryList" and "fileList"
        when exception return None
    """
    try:
        if hdfs_path == '' or hdfs_path is None:
            logger.error('parameter hdfs_path is empty')
            return False
        res_dict_list = list(hdfs_client.ls([hdfs_path]))
        directory_list = []
        file_list = []
        for item_dict in res_dict_list:
            if item_dict['file_type'] == 'd':
                directory_list.append(item_dict['path'])
            else:
                file_list.append(item_dict['path'])
        return {
            'directoryList': directory_list,
            'fileList': file_list
        }
    except Exception,e:
        logger.error('list hdfs path:[%s] exception:[%s]' % (hdfs_path, str(e)))
        return None

def mkdir(hdfs_path):
    """
    Make hdfs directory

    Parameters:
        @hdfs_path –- HDFS path

    Returns:
        return True/False
    """
    try:
        if hdfs_path == '' or hdfs_path is None:
            logger.error('parameter hdfs_path is empty')
            return False
        gen = hdfs_client.mkdir([hdfs_path], create_parent=True)
        res_dict = gen.next()
        if res_dict['result'] == False:
            logger.error('make hdfs directory:[%s] error:[%s]' % (hdfs_path, res_dict['error']))
            return False
        return True
    except Exception,e:
        logger.error('make hdfs directory:[%s] exception:[%s]' % (hdfs_path, str(e)))
        return False

def mv(src_path, dst_path):
    """
    Move source hdfs path to destination hdfs path

    Parameters:
        @src_path –- source HDFS path
        @dst_path –- destination HDFS path

    Returns:
        return True/False
    """
    try:
        if src_path == '' or src_path is None or \
            dst_path == '' or dst_path is None:
            logger.error('parameter src_path or dst_path is empty')
            return False
        gen = hdfs_client.rename([src_path], dst_path)
        res_dict = gen.next()
        if res_dict['result'] == False:
            logger.error('move source path:[%s] to destnation path:[%s] error:[%s]' % (src_path, dst_path, res_dict['error']))
            return False
        return True
    except Exception,e:
        logger.error('move source path:[%s] to destnation path:[%s] exception:[%s]' % (src_path, dst_path, str(e)))
        return False

def rmdir(hdfs_path):
    """
    Remove hdfs path

    Parameters:
        @hdfs_path –- HDFS directory

    Returns:
        return True/False
    """
    try:
        if hdfs_path == '' or hdfs_path is None:
            logger.error('parameter hdfs_path is empty')
            return False
        gen = hdfs_client.delete([hdfs_path], recurse=True)
        res_dict = gen.next()
        if res_dict['result'] == False:
            logger.error('remove hdfs directory:[%s] error:[%s]' % (hdfs_path, res_dict['error']))
            return False
        return True
    except Exception,e:
        logger.error('remove hdfs directory:[%s] exception:[%s]' % (hdfs_path, str(e)))
        return False

def exists(hdfs_path):
    """
    Check hdfs path is exists support directory and file

    Parameters:
        @hdfs_path –- HDFS path

    Returns:
        return True/False
    """
    try:
        if hdfs_path == '' or hdfs_path is None:
            logger.error('parameter hdfs_path is empty')
            return False
        return hdfs_client.test(hdfs_path)
    except Exception,e:
        exception_str = str(e)
        if exception_str.find('No such file or directory') > 0:
            return False
        logger.error('check hdfs path:[%s] exists exception:[%s]' % (hdfs_path, exception_str))
        return False

def touch(hdfs_file):
    """
    Touch hdfs file when has exists straight return

    Parameters:
        @hdfs_file –- HDFS file

    Returns:
        return True/False
    """
    try:
        if hdfs_file == '' or hdfs_file is None:
            logger.error('parameter hdfs_file is empty')
            return False
        if exists(hdfs_file):
            return True
        gen = hdfs_client.touchz([hdfs_file])
        res_dict = gen.next()
        if res_dict['result'] == False:
            logger.error('touch hdfs file:[%s] error:[%s]' % (hdfs_file, res_dict['error']))
            return False
        return True
    except Exception,e:
        logger.error('touch hdfs file:[%s] exception:[%s]' % (hdfs_file, str(e)))
        return False
