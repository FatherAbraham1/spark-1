#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from pyspark import SparkContext
sc = SparkContext("Spark_0_code")

def example_0():
    text_file = sc.textFile("hdfs://...")
    counts = text_file.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
    counts.saveAsTextFile("hdfs://...")

def main():
    pass

if __name__ == "__main__":
    try:
        main()
    except Exception,e:
        print "Spark main function exception:[%s]" % str(e)
        sys.exit(2)
