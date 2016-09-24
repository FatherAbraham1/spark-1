## 1.简介 
这篇文章主要是简单的介绍一下Spark应用如何在集群上运行, 更进一步的理解Spark所涉及到的相关主件

## 2.架构
Spark应用在集群上是独立运行的进程, 通过主程序(main program)的SparkContext进行协调. 一般我们成Spark的主程序为driver程序(driver program)

特别的, 在集群上运行Spark, SparkContext对象支持和多种不同类型的集群管理器(Cluster manager)进行通信. 包括Spark自己的standalone集群管理器, Mesos还有YARN. SparkContext和Cluster manager连接之后, Cluster manager会在集群的worker节点上启动executor进程(真正进行数据处理, 计算和存储), 接下来把应用程序的代码(JAR包或这所Python文件)发送到executor进程, 最后SparkContext发送tasks到executor进程上去执行

上诉的流程, 简单用几个步骤进行描述

1. SparkContext和Cluster manager通信
2. Cluster manager在集群的worker节点启动executor进程
3. Cluster manager把Spark应用代码发送给executor进程
4. SparkContext推送task到executor上执行

![](http://spark.apache.org/docs/latest/img/cluster-overview.png)

从上图可以看出

1. SparkContext负责驱动整个Spark应用的执行
2. Cluster manager负责进行资源分配和任务调度(executros启动)
3. executor负责执行Spark的task任务

对于这个架构, 有几个我们必须了解

1. 每个应用的executor进程所相互隔离的, executor进程贯穿于整个应用的生命周期, 同时用多线程执行task. executor进程隔离有什么好处呢? 第一点对于driver调度来说, 每个driver只管负责调度自己的task即可. 第二点对于executor执行来说不同的应用的task运行在不同JVM. 相反, 进程隔离意味着不同Spark应用程序之间的数据无法共享, 除了持久化存储的那些数据
2. 对于Spark来说并不关心Cluster manager, 只要能够启动executor进程同时也能够互相通信就可以. 对于Mesos/YARN来说非常容易运行其他运用程序, 包括Spark
3. Spark的整个生命周期期间, driver程序需要监听并且接收外部请求. 因此必须保证driver程序网络可用
4. 由于driver程序要调度task到worker节点的executor进程运行, 因此driver程序应该和worker节点在同一个集群内执行. 如果想发送一个请求到远程集群, 最好通过发送RPC请求来提交相关操作

## 3.Clsuter manager
目前有三种类型的Cluster manager支持Spark

[standalone]: http://spark.apache.org/docs/latest/spark-standalone.html
[Apache Mesos]: http://spark.apache.org/docs/latest/running-on-mesos.html
[Hadoop YARN]: http://spark.apache.org/docs/latest/running-on-yarn.html

## 4.名词解释
Spark应用程序可以通过 spark-submit进行提交

每个driver程序都有一个web UI, 端口4040. 前端可以展示tasks, executors和存储使用情况.

Term              Meaning
----------------------------------------------------------------------------------
Application       用户开发的Spark应用程序, 包括driver程序和集群的executors进程
----------------------------------------------------------------------------------
Application jar   包含用户Spark应用程序的jar包, 有些时候用户创建一个jar包, 包含应用
                  所有的依赖项. 但是用户的jar包不应该包括Hadoop或者Spark相关的库
----------------------------------------------------------------------------------
Driver program    应用程序执行main函数的进程, 同时生成SparkContext
----------------------------------------------------------------------------------
Cluster manager   集群服务用于分配资源
----------------------------------------------------------------------------------
Deploy mode       driver程序运行的区别. "cluster"模式, driver程序运行在集群的任意wroker
                  节点. "client"模式, driver程序运行在本地
----------------------------------------------------------------------------------
Worker node       集群的任何一个可以执行应用的节点
----------------------------------------------------------------------------------
Executor          每个应用在worker节点上启动的一个进程, 执行task任务同时把数据放在
                  内存或者磁盘. 每个应用都有自己的executor进程
----------------------------------------------------------------------------------
Task              executor执行的一个单元
----------------------------------------------------------------------------------
Job               多个并行计算task组成一个Job
----------------------------------------------------------------------------------
Stage             每个job被分割成多个不同task集合, 每个task集合称为stage
                  例如map和reduce是Mapeduce的一个stage



