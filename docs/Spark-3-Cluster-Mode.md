## 1.简介 
这篇文章主要是简单的介绍一下Spark应用如何在集群上运行, 更进一步的理解Spark所涉及到的相关主件

## 2.主件介绍
Spark应用在集群上是独立运行的进程, 通过主程序(main program)的SparkContext进行协调. 一般我们成Spark的主程序为driver程序(driver program)

特别的, 在集群上运行Spark, SparkContext对象支持和多种不同类型的集群管理器(Cluster managers)进行通信. 包括Spark自己的standalone集群管理器, Mesos还有YARN. SparkContext和Cluster managers连接之后, Cluster managers会在集群的worker节点上启动executors进程(真正进行数据处理, 计算和存储), 接下来把应用程序的代码(JAR包或这所Python文件)发送到executors进程, 最后SparkContext发送tasks到executors进程上去执行

上诉的流程, 简单用几个步骤进行描述
1. SparkContext和Cluster managers通信
2. Cluster managers在集群的worker节点启动executors进程
3. Cluster managers把Spark应用代码发送给executors进程
4. SparkContext推送task到executors上执行

![](http://spark.apache.org/docs/latest/img/cluster-overview.png)

从上图可以看出
1. SparkContext负责驱动整个Spark应用的执行
2. Cluster managers负责进行资源分配和任务调度(executros启动)
3. executors负责执行Spark的task任务


