"""
Simple spark app
"""

from pyspark import SparkContext
sc = SparkContext("local", "SimpleApp")

#Spark default read from HDFS
#must be sure has exist HDFS file /user/hadoop/test_data/README.md
data_rdd = sc.textFile('/user/hadoop/test_data/README.md').cache()
num_a = data_rdd.filter(lambda line: 'a' in line).count()
num_b = data_rdd.filter(lambda line: 'b' in line).count()
print "============================"
print num_a
print num_b
print "============================"
