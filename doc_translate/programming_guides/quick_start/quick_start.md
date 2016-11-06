## 1. 概览
这篇文章主要是关于Spark的快速熟悉和使用，我们使用Python和Spark的shell接口来操作Spark。
Spark shell使得我们可以很简单的学习Spark的Api，同时也是一个强大数据分析交互的工具。

## 2. Spark shell
我们使用Python版本的Spark工具pyspark，前提是Spark的安装路径已经加到环境变量PATH中，否则会报找不到命令
特别说明: >>>表示的所pyspark的命令

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
```
>>> textFile.count()
4
>>> textFile.first()
u'spark'
```

3). RDD transformation操作
```
>>> newTextFile = textFile.filter(lambda line: "spark" in line)
>>> newTextFile.count()
1
```

4). RDD的操作支持链接在一起操作
```
>>> textFile.filter(lambda line: "spark" in line).count()
1
```

## 3. RDD更多操作
1). RDD的action和transformation可以用在更复杂的计算上面
```
>>> textFile.map(lambda line: len(line)%2).reduce(lambda a,b: a if (a > b) else b)
1
```
说明: map产生一个新的RDD,RDD每个值是一个整数,等于每一行长度的1/2.reduce产生另一个新的RDD,对于key相同的数据取整数值最大的那个.(默认情况下key都相同)

在这里我们采用的是python的lambda来代替函数, 所以上面的代码等价于下面的代码
```
>>> def max(a, b):
...     if a > b:
...             return a
...     else:
...             return b
... 
>>> textFile.map(lambda line: len(line)%2).reduce(max)
1
```

对于Hadoop的MapReduce来说,Spark可以很容易就实现,比如常见的word count
```
>>> wordCount = textFile.flatMap(lambda line: line.split('u')).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a+b)
>>> wordCount.collect()
[(u'i', 1), (u'', 1), (u'spark', 1), (u'love', 1), (u'yo', 1)]
```

在这里我用到了flatMap 这个api, 把一行映射为多行并产生一个新的RDD.再用map把映射为pair(word, 1), 最后用reduce把相同word的count相加.
我们可以用collect action以list方式输出RDD数据


## 4. 数据缓存
Spark支持把数据缓存到内存中, 很多时候当某些数据被频繁利用的时候缓存数据到内存是非常有用的. 比如当我们在计算网页PageRank的时候可以把经常用的query集合缓存到内存中

```
>>> wordCount.cache()
PythonRDD[30] at collect at <stdin>:1
>>> wordCount.count()
5
>>> wordCount.count()
5
```

## 5. Spark应用程序
同理我们也可以使用Spark API编写Spark应用程序

现在我们用Python API编写一个Spark的应用程序, 命名为simple_app.py

```
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
print num_a
print num_b
```

我们用spark-submit来提交这个应用程序
```
spark-submit --master yarn simple_app.py
```

快速的完成了Spark的第一个应用程序,后面我们会对Spark的各个模块进入更深的研究
