#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from pyspark import SparkContext
from spark_util import hdfs_util
sc = SparkContext(appName="Spark_0_code")

def main():
    """
    1. put data_0.dat to hdfs path /user/hadoop/programming_guide/spark_programming_guide/data_0.dat
    2. put data_1.dat to hdfs path /user/hadoop/programming_guide/spark_programming_guide/data_1.dat
    """
    data_directory = '/user/hadoop/programming_guide/spark_programming_guide'
    text_file = sc.textFile(data_directory)
    pickle_file_file = '/user/hadoop/programming_guide/spark_programming_guide/pickle_file.dat'
    if hdfs_util.exists(pickle_file_file) is False:
        hdfs_util.rmdir(pickle_file_file)
    #text_file.saveAsPickleFile(pickle_file_dir)
    # read pickle_file_name
    #print hdfs_util.read(pickle_file_name)

if __name__ == "__main__":
    try:
        main()
    except Exception,e:
        print "Spark main function exception:[%s]" % str(e)
        sys.exit(2)
