#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unittest
from py_util import file_util
sys.path.append('../spark_util')
import hdfs_util

class HdfsUtilTest(unittest.TestCase):
    @unittest.skip("skip cat function")
    def test_cat(self):
        hdfs_file = ''
        print hdfs_util.cat(hdfs_file)

        hdfs_file = '/user/hadoop/examples/'
        print hdfs_util.cat(hdfs_file)

        hdfs_file = '/user/hadoop/examples2/'
        print hdfs_util.cat(hdfs_file)

        hdfs_file = '/user/hadoop/examples/data_0.dat'
        print hdfs_util.cat(hdfs_file)

        hdfs_file = '/user/hadoop/examples/data_01.dat'
        print hdfs_util.cat(hdfs_file)

    @unittest.skip("skip copy_to_local function")
    def test_copy_to_local(self):
        hdfs_file_list = []
        local_path = ''
        self.assertFalse(hdfs_util.copy_to_local(hdfs_file_list, local_path))

        hdfs_file_list = []
        local_path = '/tmp/examples'
        self.assertFalse(hdfs_util.copy_to_local(hdfs_file_list, local_path))

        hdfs_file_list = ['/user/hadoop/examples/data_0.dat']
        local_path = ''
        self.assertFalse(hdfs_util.copy_to_local(hdfs_file_list, local_path))

        hdfs_file_list = ['/user/hadoop/examples/data_0.dat']
        local_path = '/tmp/examples/data_0/'
        self.assertTrue(hdfs_util.copy_to_local(hdfs_file_list, local_path))
        file_util.remove_dir('/tmp/examples')

        hdfs_file_list = ['/user/hadoop/examples/data_0.dat']
        local_path = '/tmp/examples/data_0.dat'
        self.assertTrue(hdfs_util.copy_to_local(hdfs_file_list, local_path))
        file_util.remove_dir('/tmp/examples')

        hdfs_file_list = ['/user/hadoop/examples/data_0.dat']
        local_path = 'data_0.dat'
        self.assertTrue(hdfs_util.copy_to_local(hdfs_file_list, local_path))
        file_util.remove_file('data_0.dat')

        hdfs_file_list = ['/user/hadoop/examples/data_0.dat']
        local_path = '.'
        self.assertTrue(hdfs_util.copy_to_local(hdfs_file_list, local_path))
        file_util.remove_file('data_0.dat')

        hdfs_file_list = ['/user/hadoop/examples/data_0.dat', '/user/hadoop/examples/data_1.dat']
        local_path = '/tmp/examples'
        self.assertTrue(hdfs_util.copy_to_local(hdfs_file_list, local_path))
        file_util.remove_dir('/tmp/examples')

        hdfs_file_list = ['/user/hadoop/examples/data_0.dat', '/user/hadoop/examples/data_1.dat']
        local_path = '/tmp/examples/'
        self.assertTrue(hdfs_util.copy_to_local(hdfs_file_list, local_path))
        file_util.remove_dir('/tmp/examples/')

        hdfs_file_list = ['/user/hadoop/examples/data_0.dat', '/user/hadoop/examples/data_1.dat']
        local_path = 'examples'
        self.assertTrue(hdfs_util.copy_to_local(hdfs_file_list, local_path))
        file_util.remove_dir('examples')

        hdfs_file_list = ['/user/hadoop/examples/data_0.dat', '/user/hadoop/examples/data_1.dat']
        local_path = '.'
        self.assertTrue(hdfs_util.copy_to_local(hdfs_file_list, local_path))

    @unittest.skip("skip count function")
    def test_count(self):
        hdfs_path = ''
        print hdfs_util.count(hdfs_path)

        hdfs_path = '/user/hadoop2/'
        print hdfs_util.count(hdfs_path)

        hdfs_path = '/user/hadoop/'
        print hdfs_util.count(hdfs_path)

        hdfs_path = '/user/hadoop/examples/data_0.dat'
        print hdfs_util.count(hdfs_path)

        hdfs_path = '/user/hadoop/examples/data_3.dat'
        print hdfs_util.count(hdfs_path)

    @unittest.skip("skip delete function")
    def test_delete(self):
        hdfs_path = ''
        self.assertFalse(hdfs_util.rm(hdfs_path))

        hdfs_path = '/user/hadoop2/'
        self.assertFalse(hdfs_util.rm(hdfs_path))

        hdfs_path = '/user/hadoop/examples/data_0.dat'
        self.assertTrue(hdfs_util.rm(hdfs_path))

    @unittest.skip("skip ls function")
    def test_ls(self):
        hdfs_path = ''
        print hdfs_util.ls(hdfs_path)

        hdfs_path = '/user/hadoop2/'
        print hdfs_util.ls(hdfs_path)

        hdfs_path = '/user/hadoop/examples'
        print hdfs_util.ls(hdfs_path)

        hdfs_path = '/user/hadoop/examples/data_1.dat'
        print hdfs_util.ls(hdfs_path)

    @unittest.skip("skip mkdir function")
    def test_mkdir(self):
        hdfs_path = ''
        self.assertFalse(hdfs_util.mkdir(hdfs_path))

        hdfs_path = '/user/hadoop'
        self.assertFalse(hdfs_util.mkdir(hdfs_path))

    @unittest.skip("skip mv function")
    def test_mv(self):
        src_path = ''
        dst_path = ''
        self.assertFalse(hdfs_util.mv(src_path, dst_path))

        src_path = ''
        dst_path = '/user/hadoop/examples/data_100.dat'
        self.assertFalse(hdfs_util.mv(src_path, dst_path))

        src_path = '/user/hadoop/examples/data_100.dat'
        dst_path = ''
        self.assertFalse(hdfs_util.mv(src_path, dst_path))

        src_path = '/user/hadoop/examples/data_1.dat'
        dst_path = '/user/hadoop/examples/data_100.dat'
        self.assertTrue(hdfs_util.mv(src_path, dst_path))

        src_path = '/user/hadoop/examples/data_100.dat'
        dst_path = '/user/hadoop/examples/data_0.dat'
        self.assertTrue(hdfs_util.mv(src_path, dst_path))

        src_path = '/user/hadoop/examples/data_100.dat'
        dst_path = '/user/hadoop/examples/data_0.dat'
        self.assertFalse(hdfs_util.mv(src_path, dst_path))

    @unittest.skip("skip rmdir function")
    def test_rmdir(self):
        hdfs_path = ''
        self.assertFalse(hdfs_util.rmdir(hdfs_path))

        hdfs_path = '/user/hadoop2'
        self.assertFalse(hdfs_util.rmdir(hdfs_path))

        hdfs_path = '/uesr'
        self.assertTrue(hdfs_util.rmdir(hdfs_path))

    @unittest.skip("skip exists function")
    def test_exists(self):
        hdfs_path = ''
        self.assertFalse(hdfs_util.exists(hdfs_path))

        hdfs_path = '/user/hadoop2'
        self.assertFalse(hdfs_util.exists(hdfs_path))

        hdfs_path = '/user/hadoop'
        self.assertTrue(hdfs_util.exists(hdfs_path))

        hdfs_path = '/user/hadoop/examples/data_0.dat'
        self.assertTrue(hdfs_util.exists(hdfs_path))

    @unittest.skip("skip touch function")
    def test_touch(self):
        hdfs_path = ''
        self.assertFalse(hdfs_util.touch(hdfs_path))

        hdfs_path = '/user/hadoop/programming_guide/spark_programming_guide/data_10000.dat'
        self.assertTrue(hdfs_util.touch(hdfs_path))

        hdfs_path = '/user/hadoop/programming_guide/spark_programming_guide/data_10001.dat'
        self.assertTrue(hdfs_util.touch(hdfs_path))

if __name__ == '__main__':
    unittest.main()
