## 1.Overview
每个Spark应用程序包含一个`driver program`用来运行用户的`main`函数并且在集群上运行各种并发操作. Spark核心是`弹性分布式数据集`(RDD), 可以在集群的节点上进行并行操作. RDD可以通过Hadoop文件系统或着任何Hadoop支持的文件系统的文件产生而来, 或者通过的已有的转换而来. 用户经常会需要把RDD缓存在内存里被重复的使用. 最后RDD在节点上支持失败自动恢复

Spark的第二个核心是`shared variables`, 可以被并行操作. 默认情况下Spark会在不同的节点上并行运行一序列函数任务, 在每个任务的函数上拷贝变量. 有些时候一个变量需要被共享. Spark支持两种不同类型的`变量共享`: `broadcast variables`在所有节点上,缓存变量的值在内存里; `accumulators`变量只允许`added`, 例如counters和sums.

这篇指南主要是介绍Spark支持的几种语言的特征. 用户很容易使用Spark的shell命令 bin/spark-shell运行Scala spark 或者 bin/pyspark运行python spark.

## 2.Linking with Spark
Spark 2.0.1要求Python2.6或3.4以上. 它使用了标准的CPython接口, 所以Spark可以使用底层基于C的库比如NumPy等等.

要运行Python Spark应用, 使用bin/spark-submit脚本. 这个脚本会加载Spark Java/Scala库并且允许提交应用程序到集群. 用户也可以使用bin/pyspark使用Python shell接口

如果要使用HDFS数据, 需要把PySpark链接到HDFS版本. 

最后, 如果应用程序想要import一些Sprak的classese, 可以参考下面方式
```
from pyspark import SparkContext, SparkConf
```

PySpark要求运行driver程序和worker节点的Python版本一致. 它使用的是环境变量PATH配置的python版本, 用户可以使用PYSPARK_PYTHON设置Python版本, 例如
```
$ PYSPARK_PYTHON=python3.4 bin/pyspark
$ PYSPARK_PYTHON=/opt/pypy-2.5/bin/pypy bin/spark-submit examples/src/main/python/pi.py
```

## 3.Initializing Spark
编写Spark应用的第一件事是产生一个[SparkContext](http://spark.apache.org/docs/latest/api/python/pyspark.html#pyspark.SparkContext)对象, 用来告诉Spark如何和集群进行通信. 产生一个SparkContext对象首先要求用户构造一个[SparkConf](http://spark.apache.org/docs/latest/api/python/pyspark.html#pyspark.SparkConf)对象包含应用的基本信息.
```
conf = SparkConf().setAppName(appName).setMaster(master)
sc = SparkContext(conf=conf)
或
sc = SparkContext(appName="appName")
```
`appName`参数表示的是应用程序的名字
`master`是[Spark, Mesos or YARN cluster URL](http://spark.apache.org/docs/latest/submitting-applications.html#master-urls)或者是特殊的`local`在本地运行Spark模式. 
在编写代码的时候用户不应个硬编码`master`在程序内部, 可以通过[spark-submit](http://spark.apache.org/docs/latest/submitting-applications.html)提交来设置. 如果只是跑本地的测试, 可以使用"local"运行Spark应用.

## 4.Using the Shell
使用PySpark shell的时候, SparkContext已经被创建好了, 默认变量名字为`sc`, 自定义的SparkContext对象不会正常工作的. 用户可以通过 `--master` 设置context连接的master, 通过 `--py-files` 添加python .zip或.egg或py文件. 也可以通过 `--packages` 添加依赖(例如Spark Packages). 也可以 `--repositories` 参数指定任何资源库. 用户可以手动通过pip 安装任何Python依赖的库.

举例1
```
使用bin/pyspark的几个例子
./bin/pyspark --master local[4]
```

举例2
```
可以通过--py-files添加code.py到Spark可以搜索的路径下, 用户可以利用import code来使用
./bin/pyspark --master local[4] --py-files code.py
```

可以使用pyspark --help查看完整的参数列表. 在底层实现上, pyspark实际上调用的是通用的脚本[spark-submit](http://spark.apache.org/docs/latest/submitting-applications.html)

我们也可以使用IPython使用PySpark shell. PySpark要求IPython 1.0.0版本之后, 可以通过设置`PYSPARK_DRIVER_PYTHON`ipython使用pyspark
```
$ PYSPARK_DRIVER_PYTHON=ipython ./bin/pyspark
```
或者使用jupyter使用pyspark
```
$ PYSPARK_DRIVER_PYTHON=jupyter ./bin/pyspark
```

## 5.Resilient Distributed Datasets (RDDs)
Spark整个核心的理念是弹性分布式数据集`resilient distributed dataset (RDD)`, 支持并行操作的数据集. 我们有2种方式产生RDD: 在driver程序里通过已有的集合序列化`parallelizing`而来, 或者从外部存储文件产生而来, 比如HDFS/HBase或者其他的Hadoop支持的文件系统.

### 5.1 Parallelized Collections






