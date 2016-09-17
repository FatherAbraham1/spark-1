## 1.简介 
MapReduct框架从hadoop-0.23版本以后发生了重大的变革, 新的计算框架我们称为MapReudce 2.0 或者 YARN(Yet-Another-Resource-Negotiator)

这篇文章主要是简单的介绍YARN的架构, 因为后续我们都会使用YARN提交Spark程序

MapReduct 2.0最主要的变革是把`资源分配`和`任务调度`隔离. 一个全局的资源管理称为ResourceManager (RM), 同时每个应用本身有一个ApplicationMaster (AM). 应用可以是单独的Job也可用是MapReduce job或者是是一个DAG job.

ResourceManager和每个worker结点我们称为NodeManager (NM)组成数据处理框架, ResourceManager对所有应用进行资源分配,管理和调度

每个应用程序都有一个ApplicationMaster, ApplicationMaster从ResourceManager分配到资源, 在NodeManager执行和监控应用

## 2. 架构
![](https://hadoop.apache.org/docs/r2.4.1/hadoop-yarn/hadoop-yarn-site/yarn_architecture.gif)


