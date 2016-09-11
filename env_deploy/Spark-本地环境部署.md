## 一. 安装yarn伪分布式集群
### 1. 创建新用户
```
(1) 添加用户: sudo useradd -m hadoop -s /bin/bash  
(2) 修改密码: sudo passwd hadoop  
(3) 添加sudo权限: sudo adduser hadoop sudo  
(4) 注销选择hadoop用户登录  
```

### 2. 系统环境配置
```
(1) sudo apt-get update  
(2) 安装vim: sudo apt-get install vim  
(3) 安装ssh: sudo apt-get install openssh-server  
```

### 3. 安装java环境
```
(1) 安装jre和jdk: sudo apt-get install openjdk-7-jre openjdk-7-jdk  
(2) 设置环境变量JAVA_HOME: dpkg -L openjdk-7-jdk | grep '/bin/javac'  
     该命令会输出一个路径，除去路径末尾的 “/bin/javac”  
(3) vim ~/.bashrc  
     添加一行export JAVA_HOME=...  
(4) source ~/.bashrc  
(5) check java 版本: java -version  
```

### 4. 安装hadoop2
```
(1) 从http://mirror.bit.edu.cn/apache/hadoop/common/下载最新的稳定版本的hadoop，例如hadoop-2.7.3/hadoop-2.7.3.tar.gz  
(2) 安装hadoop:  
      sudo tar -zxf hadoop-2.7.3.tar.gz -C /usr/local  
      cd /usr/local  
      sudo mv hadoop-2.7.3 hadoop  
      sudo chown -R hadoop hadoop  
(3) 修改./etc/hadoop/core-site.xml文件，如下  
<configuration>  
        <property>  
             <name>hadoop.tmp.dir</name>  
             <value>file:/usr/local/hadoop/tmp</value>  
             <description>Abase for other temporary directories.</description>  
        </property>  
        <property>  
             <name>fs.defaultFS</name>  
             <value>hdfs://localhost:9000</value>  
        </property>  
</configuration>  
(4) 修改./etc/hadoop/hdfs-site.xml文件，如下  
<configuration>  
        <property>  
             <name>dfs.replication</name>  
             <value>1</value>  
        </property>  
        <property>  
             <name>dfs.namenode.name.dir</name>  
             <value>file:/usr/local/hadoop/tmp/dfs/name</value>  
        </property>  
        <property>  
             <name>dfs.datanode.data.dir</name>  
             <value>file:/usr/local/hadoop/tmp/dfs/data</value>  
        </property>  
</configuration>
(4) namenode格式化  
    ./bin/hdfs namenode -format  
(5) 修改~/.bashrc添加以下两行，并执行source ~/.bashrc  
    export HADOOP_HOME=/usr/local/hadoop   
    export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native  
(6) ./libexec/hadoop-config.sh 找到JAVA_HOME，在前面添加  
    export JAVA_HOME=...  
(7) 开启 NameNode 和 DataNode 守护进程  
    ./sbin/start-dfs.sh  
(8) jps命令查看是否成功启动  
    若成功启动则会列出如下进程: “NameNode”、”DataNode” 和 “SecondaryNameNode”（如果 SecondaryNameNode 没有启动，请运行 sbin/stop-dfs.sh 关闭进程，然后再次尝试启动尝试）。如果没有 NameNode 或 DataNode ，那就是配置不成功，请仔细检查之前步骤，或通过查看启动日志排查原因。  
(9) 启动成功后可以通过 http://localhost:50070/查看nameNode和dataNode相关信息  
(10) 关闭hadoop  
      ./sbin/stop-dfs.sh  
      第二次之后启动 hadoop，无需进行 NameNode 的初始化，只需要运行 ./sbin/start-dfs.sh 即可  
```

### 5. 启动YARN
```
(1) 重命名./etc/hadoop/mapred-site.xml文件  
      mv ./etc/hadoop/mapred-site.xml.template ./etc/hadoop/mapred-site.xml  
(2) 编辑./etc/hadoop/mapred-site.xml文件  
<configuration>  
        <property>  
             <name>mapreduce.framework.name</name>  
             <value>yarn</value>  
        </property>  
</configuration>  
(3) ./etc/hadoop/yarn-site.xml文件  
<configuration>  
        <property>  
             <name>yarn.nodemanager.aux-services</name>  
             <value>mapreduce_shuffle</value>  
            </property>  
</configuration>  
(4) 启动yarn  
      ./sbin/start-yarn.sh   
      ./sbin/mr-jobhistory-daemon.sh start historyserver  #开启历史服务器，才能在Web中查看任务运行情况  
(5) jps查看  
      开启后通过 jps 查看，可以看到多了 NodeManager 和 ResourceManager 两个后台进程  
 (6) 启动成功后可以通过页面http://localhost:8088/cluster查看集群任务的运行情况  
 (7) 关闭yarn  
       ./sbin/stop-yarn.sh   
       ./sbin/mr-jobhistory-daemon.sh stop historyserver  
```

## 二. 安装Spark
```
1. 下载Spark  
    wget "http://d3kbcqa49mib13.cloudfront.net/spark-2.0.0-bin-hadoop2.7.tgz"  
2. 解压到/usr/local  
    sudo tar -xvzf spark-2.0.0-bin-hadoop2.7.tgz -C /usr/local  
    cd /usr/local  
    sudo mv spark-2.0.0-bin-hadoop2.7 spark  
3. 设置环境变化PATH  
    vim ~/.bashrc  
    export PATH=$PATH:/usr/local/hadoop/bin:/usr/local/spark/bin  
    source ~/.bashrc  
4. 开始使用Spark  
    pyspark 或 spark-submit  
```

## 三. tools
```
1. start YARN  
cd /usr/local/hadoop  
./sbin/start-dfs.sh  
./sbin/start-yarn.sh  
./sbin/mr-jobhistory-daemon.sh start historyserver  

2. stop YARN  
cd /usr/local/hadoop  
./sbin/stop-dfs.sh  
./sbin/stop-yarn.sh  
./sbin/mr-jobhistory-daemon.sh stop historyserver 
```
