## 1. 概览
这篇文章主要是关于Spark的快速熟悉和使用，我们使用Python和Spark的shell接口来操作Spark。
Spark shell使得我们可以很简单的学习Spark的Api，同时也是一个强大数据分析交互的工具。

## 2. Spark shell
我们使用Python版本的Spark工具pyspark，前提是Spark的安装路径已经加到环境变量PATH中，否则会报找不到命令

```
./bin/pyspark
```

Spark核心的抽象是弹性分布式数据集合，我们称为RDD（Resilient Distributed Dataset）。一个RDD可以从输入文件中产生比如HDFS文件，也可以从其他RDD转换而来。

我们通过读取本地文件text.dat来创建一个新的RDD

```
hadoop@ubuntu:~/github$ cat text.dat
spark
i
love
you
```

```
>>> textFile = sc.textFile("text.dat")
```

RDD包括两种运算操作，action和transformation。action操作会返回值，例如count()，transformation操作则是返回一个新的RDD，例如filter()。

2). RDD action操作



3). RDD transformation操作



4). RDD的操作支持链接在一起操作



## 3. RDD更多操作
1). RDD的action和transformation可以用在更复杂的计算上面




