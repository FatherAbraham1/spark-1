#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from pyspark import SparkContext
sc = SparkContext(appName="Spark_0_code")

def example_one():
    """
    1. first put data_0.dat to hdfs path /user/hadoop/examples/data_0.dat
    """
    raw_data_file = '/user/hadoop/examples/data_0.dat'
    text_file = sc.textFile(raw_data_file)
    print text_file.collect()
    new_text_file = text_file.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
    result_data_path = '/user/hadoop/examples/data_0_res'
    new_text_file.saveAsTextFile(result_data_path)

def main():
    example_one()

if __name__ == "__main__":
    try:
        main()
    except Exception,e:
        print "Spark main function exception:[%s]" % str(e)
        sys.exit(2)
