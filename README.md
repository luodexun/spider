#Kete Spider
第一步：创建xxx项目
scrapy startproject ***

第二步：创建要抓取的名称及抓取网址
scrapy genspider *** 'https://hr.tencent.com/position.php'

第三步：编写items.py，明确需要提取的数据

第四步：编写spiders/xxx.py 编写爬虫文件，处理请求和响应，以及提取数据（yeild item）

第五步：编写pipelines.py管道文件，处理spider返回item数据

第六步：编写settings.py，启动管理文件，以及其他相关设置
ITEM_PIPELINES = {
    'cententjob.pipelines.CententjobPipeline': 300,
}
第七步：执行爬虫
scrapy crawl ***

###[python whl库，windows安装必备！！！](https://www.lfd.uci.edu/~gohlke/pythonlibs/)


###虚拟环境安装依赖：  
source /root/venv_spider/bin/activate  
pip3.6 install xxx  

###运行爬虫：  
/root/venv_spider/bin/python3.6 run.py wechat  

###部署定时任务：  
1. kete_airflow/dags下面添加dags文件
2. 服务器上cp kete_airflow/dags/* ~/airflow/dags
3. 5分钟后刷新airflow后台 http://121.201.55.116:8080/admin/ 打开开关，手动执行dag命令，看看是否正常

###添加azkaban爬虫任务
1. 复制azkaban_jobs/spiders内 run_ifeng_spider.job
2. 修改文件名为对应爬虫名，修改文件内command命令对应的爬虫名
3. 压缩job文件，或者整个spiders文件夹，zip格式
4. 访问 http://121.201.55.116:18081/manager?project=run_spiders 上传zip文件
5. 找到新添加的任务，点击execution flow，点击execute执行一下，运行success后，修改schedule  

爬虫运行统一使用的 scripts/run_spider.sh脚本调用python，如果运行其他定时任务，需要自行编写shell脚本

安装依赖
pip3.6 install xxxxxx
pip3.6 install -r requirements.txt
pip freeze >> requirements.txt

