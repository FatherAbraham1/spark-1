## 1.Spark overview 
Apache Spark是一个快速且通用的分布式并行计算框架，它提供了Java, Scala, Python 和 R 这四种语言的API，同时提供了一个最佳的图执行引擎。同时它也提供了很多工具，Spark-SQL用来提供SQL和结构化数据处理；MLlib是Spark的机器学习库；Graph X用来进行图计算；Spark Streaming则提供数据的流式处理。

## 2.Downloading
[Spark下载页面](http://spark.apache.org/downloads.html)下载Spark. 这个文档是Spark版本2.0.1. Spark使用Hadoop Client库因为HDFS和YARN. 下载之前必须先下载好可靠的Hadoop版本. 用户可以下载一个"Hadoop free"二进制同时执行Spark通过任何的Hadoop版本使用[Spark classpath参数](http://spark.apache.org/docs/latest/hadoop-provided.html)

用户也可以自己使用源码build Spark, 参考[Building Spark](http://spark.apache.org/docs/latest/building-spark.html)

Spark可以在Windows和类Unix系统(Linux, Mac Os 等等). Spark也很容易在一台本地机器上执行, 但是要求系统必须安装java, 同时也要求环境变量PATH能够正常找到Java安装环境

Spark可以运行在Java 版本7.0以上, Python 2.6或3.4以上 或 R 3.1以上. 对于Scala API, Spark 2.0.1 使用的四Scala 2.11, 所以要求使用兼容的2.11.x版本

## 3.Running the Examples and Shell
Spark 提供了几个简单的程序. Scala, Java, Python 和 R 程序例子在examples/src/main 目录下. 运行Java或Scala例子程序, 在Spark顶级目录下运行命令bin/run-example <class> [params]. (在后端使用的都是spark-submit脚本进行应用程序的提交)


例子1
```
./bin/run-example SparkPi 10
```

例子2
```
./bin/spark-shell --master local[2]

--master参数指定[分布式集群master url](http://spark.apache.org/docs/latest/submitting-applications.html#master-urls), 参数值local表示在本地运行, local[N]表示的是使用N个线程运行. 如果要测试Spark应用, 我们应该使用local master. 可以使用Spark shell命令的--help参数获取整个参数列表.

```

例子3
```
Python Spark应用，例如
./bin/spark-submit examples/src/main/python/pi.py 10

```

例子4
```
Spark 1.4版本之后提供一个R的API
./bin/sparkR --master local[2]

同时也可也使用spark-submit
./bin/spark-submit examples/src/main/r/dataframe.R
```

## 3. Launching on a Cluster
Spark [集群模式总结](http://spark.apache.org/docs/latest/cluster-overview.html)介绍了Spark在集群运行的重要概念. Spark可以自主运行, 也可以在几个不同的集群管理器下运行. 现在提供了几个不同的集群运行环境

1. [Standalone Deploy Mode](http://spark.apache.org/docs/latest/spark-standalone.html) 最简单的在私有集群上部署Spark的方式
2. [Apache Meson](http://spark.apache.org/docs/latest/running-on-mesos.html)
3. [Hadoop YARN](http://spark.apache.org/docs/latest/running-on-yarn.html)

## 4. Where to Go from Here
### 1. Programming guides
1. [Quick Start](http://spark.apache.org/docs/latest/quick-start.html) 从这里快速了解Spark API
2. [Spark Programming Guide](http://spark.apache.org/docs/latest/programming-guide.html) 细节总结Spark支持的四种语言(Scala, Java, Python, R)
3. Spark 内置模块
   1. [Spark Streaming](http://spark.apache.org/docs/latest/streaming-programming-guide.html) Spark实时流式处理
   2. [Spark SQL, Datasets and DataFrames](http://spark.apache.org/docs/latest/sql-programming-guide.html) 结构化和关系型数据处理
   3. [MLlib](http://spark.apache.org/docs/latest/ml-guide.html) Spark内置机器学习库
   4. [Graphx](http://spark.apache.org/docs/latest/graphx-programming-guide.html) Spark图处理Api

### 2. API Docs
1. [Spark Scala API](http://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.package)
2. [Spark Java API](http://spark.apache.org/docs/latest/api/java/index.html)
3. [Spark Python API](http://spark.apache.org/docs/latest/api/python/index.html)
4. [Spark R API](http://spark.apache.org/docs/latest/api/R/index.html)

### 3. Deployment Guides
1. [Cluster Overview](http://spark.apache.org/docs/latest/cluster-overview.html) 总结集群上运行的重要的概念和组件介绍
2. [Submitting Applications](http://spark.apache.org/docs/latest/submitting-applications.html) 打包和部署应用
3. Deployment modes
   1. [Amazon EC2](https://github.com/amplab/spark-ec2) 5分钟带你了解在EC2部署集群 
   2. [Standalone Deploy Mode](http://spark.apache.org/docs/latest/spark-standalone.html) 独立部署Spark集群, 无需依靠第三方的集群管理器
   3. [Mesos](http://spark.apache.org/docs/latest/running-on-mesos.html) 使用Apache Meson部署私有集群
   4. [YARN](http://spark.apache.org/docs/latest/running-on-yarn.html) 在YARN上使用Spark
   
### 4. Other Documents
1. [Configuration](http://spark.apache.org/docs/latest/configuration.html) 定制化配置Spark集群
2. [Monitoring](http://spark.apache.org/docs/latest/monitoring.html) 应用追踪和监控
3. [Tuning Guide](http://spark.apache.org/docs/latest/tuning.html) 优化性能和内存使用最佳实践
4. [Job Scheduing](http://spark.apache.org/docs/latest/job-scheduling.html) Spark应用程序之间的资源调度
5. [Security](http://spark.apache.org/docs/latest/security.html) Spark安全
6. [Hardware Provisioning](http://spark.apache.org/docs/latest/hardware-provisioning.html) Spark集群硬件推荐
7. 其他存储系统
   1. [OpenStack Swift](http://spark.apache.org/docs/latest/storage-openstack-swift.html)
8. [Building Spark](http://spark.apache.org/docs/latest/building-spark.html) 使用Maven build Spark
9. [Contributing to Spark](https://cwiki.apache.org/confluence/display/SPARK/Contributing+to+Spark)
10. [Third Party Project](https://cwiki.apache.org/confluence/display/SPARK/Third+Party+Projects) Spark相关第三方项目

### 5. External Resources
1. [Spark Homepage](http://spark.apache.org/)
2. [Spark Wiki](https://cwiki.apache.org/confluence/display/SPARK)
3. [Spark Community](http://spark.apache.org/community.html)
4. [StackOverflow tag apache-spark](http://stackoverflow.com/questions/tagged/apache-spark)
5. [Mailing Lists](http://spark.apache.org/mailing-lists.html)
6. [AMP Camps](http://ampcamp.berkeley.edu/)
7. [Code Examples](http://spark.apache.org/examples.html)



