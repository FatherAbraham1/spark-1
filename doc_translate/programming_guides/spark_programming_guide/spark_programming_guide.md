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
我们可以在driver程序使用`SparkContext`对象的`parallelize`方法从已有的迭代器(iterable)或数据集(collections)并行化数据, 并行化数据支持分布式并行操作并行操作. 例如, 下面这个例子从数据集合[1~5]产生并行化数据
```
data = [1, 2, 3, 4, 5]
distData = sc.parallelize(data)

parallelize函数返回一个RDD对象
```

一旦调用parallelize函数会返回一个RDD对象, 可以被并行操作. 例如, 我们可以使用`distData.reduct(lambda a,b: a+b)`计算所有elements的和.

`parallelize`函数有一个很重要的参数可以设置分割数据集为几个partition. Spark集群一个task处理一个partition. 典型的你可能希望集群的每一个CPU处理2-4个partition. 一般情况下, 不设置的话, Spark会尝试自动根据集群设置partition的个数. 用户也可以使用`parallelize(data, 10)`设置10个partition.

注意: 有些代码API会使用`slices`代替`partitions`表示设置patition的个数

### 5.2 External Datasets
PySpark可以从任何Hadoop支持的文件系统文件产生分布式数据集, 包括本地文件系统, HDFS, Cassandra, HBase, Amazon S3等等. Spark支持text files, SequenceFiles 和任何Hadoop输入格式文件. 

可以使用SparkContext对象的`textFile`函数从text file生成RDD对象. 函数需要一个文件URI参数(包括机器本地文件路径或者hdfs文件路径或者其他...), 函数会一行一行读取文件, 例如下面这个例子
```
>>> distFile = sc.textFile("data.txt")
```
distFile一旦产生可以支持各种数据操作. 例如, 我们可以好似用`map`和`reduct`操作计算总的字符数`distFile.map(lambda s: len(s)).reduce(lambda a,b:a+b)`

Spark读取文件需要注意的几个点
1. 如果读取的文件来自本地文件系统, 要求所有的worker节点都包含有相同的路径. 可以通过拷贝文件到所有的worker节点或者使用`network-mounted`共享文件.
2. 所有Spark基于文件的输入函数, 包括`textFile`都支持配置到目录级别, 压缩文件和通配符. 例如, 用户可以设置`textFile("/my/directory")`或者`textFile("/my/directory/*.txt")`或者`textFile("/my/directory/*.gz")`
3. `textFile`函数支持可选的第二个参数设置paritition的个数. 默认情况下, 每个`block`对应生成一个partition(HDFS默认情况一个block是64M), 但是用户也可以设置更大的partition个数, 不过需要注意的是partition的个数不能比block的个数还少.

除了text file文件格式, Spark Python API也支持其他几种数据格式
1. `SparkContext.wholeTextFiles` 支持读取一个包含多个text file的目录, 同时返回一序列<fileName, content> pairs, 假设有n个文件, 因此在使用collect函数的时候会返回n个元素的list对象. `textFile`则是顺序把所有的文件一行一行的读取, 假设所有文件总共有m行, 使用collect函数的会返回一个m个元素的list对象. 具体可以看下面这个代码
```
'''
1. put data_0.dat to hdfs path /user/hadoop/programming_guide/spark_programming_guide/data_0.dat
2. put data_1.dat to hdfs path /user/hadoop/programming_guide/spark_programming_guide/data_1.dat
'''
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

代码: ./code/Spark_0_code.py
提交: spark-submit  --master yarn --num-executors 1 --executor-cores 2 --executor-memory 500M Spark_0_code.py
      默认用client方式执行这样才能在当前机器看到print信息
      spark-submit  --master yarn --deploy-mode cluster --num-executors 1 --executor-cores 2 --executor-memory 500M Spark_0_code.py
      这种方式执行的话driver print的信息不会打在当前机器的console
```
2. `RDD.saveAsPickleFile`和`SparkContext.pickleFile`支持保存RDD对象为串行的Python对象, SparkContext.pickleFile底层调用的是RDD.saveAsPickleFile, 序列化RDD为一个SequenceFile, 默认batch大小为10
3. 读写`SequenceFile`文件

### 5.1.1 Saving and Loading SequenceFiles
和`text files`一样, Spark也支持保存和读写一个`SequenceFiles`文件. 可以指定特殊的key和value, 但是对于一般的标准写来说并不需要设置key和value
SequenceFile是Hadoop API 提供的一种二进制文件，它将数据以<key,value>的形式序列化到文件中。这种二进制文件内部使用Hadoop 的标准的Writable 接口实现序列化和反序列化。它与Hadoop API中的MapFile 是互相兼容的。Hive 中的SequenceFile 继承自Hadoop API 的SequenceFile，不过它的key为空，使用value 存放实际的值， 这样是为了避免MR 在运行map 阶段的排序过程。如果你用Java API 编写SequenceFile，并让Hive读取的话，请确保使用value字段存放数据，否则你需要自定义读取这种SequenceFile 的InputFormat class 和OutputFormat class。
```
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

a.saveAsSequenceFile生成的是目录
b.可以用SparkContext对象的sequenceFile函数读取sequence file

代码: ./code/Spark_1_code.py
提交: spark-submit  --master yarn --num-executors 1 --executor-cores 2 --executor-memory 500M Spark_1_code.py
```

### 5.1.2 Saving and Loading Other Hadoop Input/Output Formats
Spark兼容了`新`,`老`Hadoop MapReduce Api任何输入或输出格式.如果需要的话, Hadoop的配置可以使用Python的dict进行配置.
```
$ SPARK_CLASSPATH=/path/to/elasticsearch-hadoop.jar ./bin/pyspark
conf = {"es.resource" : "index/type"}   # assume Elasticsearch is running on localhost defaults
rdd = sc.newAPIHadoopRDD("org.elasticsearch.hadoop.mr.EsInputFormat",\
    "org.apache.hadoop.io.NullWritable", "org.elasticsearch.hadoop.mr.LinkedMapWritable", conf=conf)
rdd.first()         # the result is a MapWritable that is converted to a Python dict
'''
    (u'Elasticsearch ID',
    {u'field1': True,
     u'field2': u'Some Text',
     u'field3': 12345})'
'''
```

### 5.2 RDD Operations
`RDD`支持2种类型操作
1. `transformations`: 从一个已有的RDD转换生成一个新的RDD
2. `actions`: 对RDD计算之后返回一个数值到driver程序
例如,`map`是一个`transformation`操作,对RDD的每一个元素进行同一个函数操作,返回一个新的RDD. 另一方面, `reduce`是一个`action`操作, 对RDD的每一个元素进行同一个元素的操作,最终返回一个结果到driver程序.注意`reduceByKey`函数是一个transformation操作,会返回一个新的RDD

Spark里的`transformations`都是延迟操作, 它们并不会马上执行. Spark会记录所有的transformations链, 当有action操作的时候再执行操作, 最终返回结果到driver程序.这个设计对于Spark来说是非常高效的, 例如使用map再用reduce返回数值的时候, 使用延迟操作可以使得map操作的数据集比较小, 如果一开始就计算map则数据集则非常大.

默认情况下, 每个action操作都会重新计算RDD. 但是,很多情况我们会希望把一个RDD缓存到内存中, 使得RDD的元素能够被更快速的使用. 除此之外, 也支持把一个RDD持久化到磁盘同时支持在多个节点备份数据.

