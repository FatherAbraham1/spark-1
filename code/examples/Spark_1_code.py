#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import random
from pyspark import SparkContext
from spark_util import hdfs_util
sc = SparkContext(appName="Spark_1_code")

def sample(p):
    x, y = random.random(), random.random()
    return 1 if x*x + y*y < 1 else 0

def main():
    NUM_SAMPLES = 30000
    count = sc.parallelize(xrange(0, NUM_SAMPLES)).map(sample).reduce(lambda a, b: a + b)
    print "Pi is roughly %f" % (4.0 * count / NUM_SAMPLES)

if __name__ == "__main__":
    try:
        main()
    except Exception,e:
        print "Spark main function exception:[%s]" % str(e)
        sys.exit(2)
