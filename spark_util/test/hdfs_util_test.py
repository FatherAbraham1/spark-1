#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unittest
sys.path.append('../spark_util')
import hdfs_util

class HdfsUtilTest(unittest.TestCase):
    def test_exists(self):
        path = '/user/hadoop/examples/'
        self.assertTrue(hdfs_util.exists(path))

        path = '/user/hadoop/examples/1'
        self.assertFalse(hdfs_util.exists(path))

        path = '/user/hadoop/examples/data_0.dat'
        self.assertTrue(hdfs_util.exists(path))

    def test_rmdir(self):
        path = '/user/hadoop/examples/data_0_res.dat'
        self.assertTrue(hdfs_util.rmdir(path))

if __name__ == '__main__':
    unittest.main()
