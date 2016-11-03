#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import random
from pyspark import SparkContext
from pyspark.sql import DataFrame
from pyspark.sql import SQLContext
from pyspark.sql.types import *

from spark_util import hdfs_util
sc = SparkContext(appName="Spark_2_code")
sqlContext = SQLContext(sc)

def main():
    """
    1. first put log_2.dat to hdfs path /user/hadoop/examples/log_2.dat
    """
    log_data_file = '/user/hadoop/examples/log_2.dat'
    text_line = sc.textFile(log_data_file)
    print text_line.collect()

    # Creates a DataFrame having a single column named "line"
    # StructField(name, dataType, nullable)
    # 代表StructType中的一个字段，字段的名字通过name指定，dataType指定field的数据类型，nullable表示字段的值是否有null值。
    schema = StructType([
        StructField("line", StringType(), True),
    ])
    df = sqlContext.createDataFrame(text_line.map(lambda r: Row(r)), schema)
    print df.collect()

    # Counts all the errors
    errors_df = df.filter(col("line").like("%error%"))
    print errors_df.collect()
    print errors_df.count()

if __name__ == "__main__":
    try:
        main()
    except Exception,e:
        print "[ERROR] Spark main function exception:[%s]" % str(e)
        sys.exit(2)
