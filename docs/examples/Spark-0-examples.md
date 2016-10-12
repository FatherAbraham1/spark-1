## 一. Spark Example
这篇文章会快速的介绍Spark的API, Spark是基于分布式的数据集, 可以包含任意的Java或Python项目. 用户可以从外部的数据生成数据集, 同时可以进行并行的操作.Spark内建的API就是RDD API. RDD API有2种操作: transformations 定义一个新的RDD基于前面的RDD; actions 在集群上开行执行job. Spark RDD提供了高级的API, DataFrame API 和 Machine Learning API. 这些API提供简单的方式进行数据操作, 在这篇文章中我们会使用这些高级的API进行演示.

## 二. RDD API Example
### 1. Word Count
这个例子中, 使用transformations去操作string pair计算word counts并存储到文件
```
text_file = sc.textFile("hdfs://...")
counts = text_file.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
counts.saveAsTextFile("hdfs://...")

a. sc.textFile用来读取hdfs文件返回RDD
b. flatMap把一个RDD数据映射为多个, map把一个单词映射为(word,1) pair, reduceByKey把相同的key进行累加
c. saveAsTextFile把RDD持久化存储到hdfs文件
```

### 2. Pi Estimation
Spark还可以执行计算密集型任务, 采取"掷非镖"的方式画出单位圆, 随机选取点(x,y)观测有多少点落于圆内, 落于圆内的概率为 pi/4, 通过这个来预测pi值
```
def sample(p):
    x, y = random(), random()
    return 1 if x*x + y*y < 1 else 0

count = sc.parallelize(xrange(0, NUM_SAMPLES)).map(sample).reduce(lambda a, b: a + b)
print "Pi is roughly %f" % (4.0 * count / NUM_SAMPLES)

a. parallelize用于把python的collection序列化为Spark的RDD, map根据随机点的位置返回1或0, reduce把所有的值相加
```

## 三. DataFrame API Example
