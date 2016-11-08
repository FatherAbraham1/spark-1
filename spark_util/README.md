## 1. 说明
Python Spark util api. Contain Python HDFS api

## 2. 使用方法
1. 修改conf目录下namenode.conf配置
2. python setup.py install
3. example: form spark_util import hdfs_util

## 3. 依赖
1. version: python2.7
2. linux: ubuntu 12.04
3. requires pkg: 
   1. py_util  --> https://github.com/chenguolin/python_util 需要用户自行install
   2. snakebite --> https://github.com/chenguolin/snakebite
4. 依赖的第三方库在install的时候会自动安装，用户无需自己安装

## 4. 基础库
1. hdfs_util: hdfs文件操作相关api
   1. cat 
   2. copy_to_local //拷贝hdfs文件或目录到本地文件系统
   3. count
   4. rm //rm hdfs file
   5. ls
   6. mkdir
   7. mv
   8. rmdir
   9. exists // check hdfs file or directory is exists
   10. touch // touch hdfs file
