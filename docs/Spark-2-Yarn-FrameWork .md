## 1.简介 
MapReduct框架从hadoop-0.23版本以后发生了重大的变革, 新的计算框架我们称为MapReudce 2.0 或者 YARN(Yet-Another-Resource-Negotiator)

这篇文章主要是简单的介绍YARN的架构, 因为后续我们都会使用YARN提交Spark程序

MapReduct 2.0最主要的变革是把`资源分配`和`任务调度`隔离. 一个全局的资源管理称为ResourceManager (RM), 同时每个应用本身有一个ApplicationMaster (AM). 应用可以是单独的Job也可用是MapReduce job或者是是一个DAG job.

ResourceManager和每个worker结点我们称为NodeManager (NM)组成数据处理框架, ResourceManager对所有应用进行资源分配,管理和调度

每个应用程序都有一个ApplicationMaster, ApplicationMaster从ResourceManager分配到资源, 在NodeManager执行和监控应用

## 2. 架构
![](https://hadoop.apache.org/docs/r2.4.1/hadoop-yarn/hadoop-yarn-site/yarn_architecture.gif)

1. ResourceManager 有2个主要的组件，调度器（Scheduler）和应用管理（ApplicationsManager）
```
(1). 调度器（Scheduler）负责分配资源给运行的应用，常见的比如容量，队列等。调度器只是单纯的进行任务的调度和资源分配，并不会监控或跟踪应用的状态。调度器负责分配资源给运行的应用，常见的比如容量，队列等。调度器只是单纯的进行任务的调度和资源分配，并不会监控或跟踪应用的状态。同时，支持重启失败任务，由于应用失败或者硬件设备问题导致。调度器满足应用程序基本的资源需求，包括`内存`, `cpu`, `磁盘`, `网络`等等。
(2). 应用管理（ApplicationsManager） 负责支持job的提交，同时启动应用的AppMaster，并且支持重启ApplicationMaster
```
2. NodeManager是每台worker机器上的一个进程，负责监控worker机器的资源使用（CPU，内存，磁盘，网络），同时把资源使用情况同步给ResourceManager 
3. 每个应用都有一个ApplicationMaster，负责和调度器进行通信申请资源，同时监控和追踪应用的状态和进度
