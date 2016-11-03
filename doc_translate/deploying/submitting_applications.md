## 1.简介
spark-submit是用来提交Spark应用到集群的脚本，它可以使用在所有支持Spark的cluster manager，并不需要针对每个进行特别的配置

如果代码依赖了其它项目，你需要把你的应用程序进行打包目的是为了分发代码到Spark集群。因此，经常需要一个“超级”jar包，包括代码和所有的依赖。
但是所有Spark和Hadoop相关的依赖都不需要打进包里，因为它们会在运行时由cluster manager提供。jar包打好之后，可以通过调用bin/spark-submit脚本进行传输。
对于Python来说可以使用sparksubmit的---py-files参数分发.py, .zip或.egg文件到集群，如果依赖了很多的Python文件，建议使用.zip或.egg进行打包

## 2.spark-submit
当用户的应用程序打包完成之后，可以通过使用bin/spark-submit进行提交。这个脚本关心class path和Spark依赖的设置，它支持不同的cluster manager同时也支持不同
的部署模式

```
./bin/spark-submit \
  --class <main-class> \
  --master <master-url> \
  --deploy-mode <deploy-mode> \
  --conf <key>=<value> \
  ... # other options
  <application-jar> \
  [application-arguments]
```
spark-submit 一些参数的解释

1. 
