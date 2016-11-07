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
    # use textFile read directory
    text_file = sc.textFile(data_directory)
    collect_res = text_file.collect()
    print type(collect_res)
    print len(collect_res)
    '''
    type<list>
    543
    '''
    # use wholeTextFiles read directory
    text_file = sc.wholeTextFiles(data_directory)
    collect_res = text_file.collect()
    print type(collect_res)
    print len(collect_res)
    '''
    type<list>
    2
    '''

if __name__ == "__main__":
    try:
        main()
    except Exception,e:
        print "Spark main function exception:[%s]" % str(e)
        sys.exit(2)
