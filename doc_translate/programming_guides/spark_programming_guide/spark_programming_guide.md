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
```
2. `RDD.saveAsPickleFile`和`SparkContext.pickleFile`支持保存RDD对象为串行的Python对象, SparkContext.pickleFile底层调用的是RDD.saveAsPickleFile, 序列化RDD为一个SequenceFile, 默认batch大小为10
```
```
3. 读写`SequenceFile`文件

