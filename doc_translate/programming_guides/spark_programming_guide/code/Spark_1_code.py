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
    """
    data_file = '/user/hadoop/programming_guide/spark_programming_guide/data_0.dat'
    text_file = sc.textFile(data_file).map(lambda x: (x, len(x)))
    # saveAsSequenceFile
    sequence_file = '/user/hadoop/programming_guide/spark_programming_guide/sequence_file'
    text_file.saveAsSequenceFile(sequence_file)
    # read sequenceFile
    res_list = sc.sequenceFile(sequence_file).collect()
    print res_list

if __name__ == "__main__":
    try:
        main()
    except Exception,e:
        print "Spark main function exception:[%s]" % str(e)
        sys.exit(2)
