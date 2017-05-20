----------------------------Created in 5.19 2017-------------------------------
1. 基于scrapy框架的爬虫系统
2. dblpSpider--给一个venue名称获得dblp名
3. dblpPaperSpider--给定一篇paper，获取paper所对应venue的dblp名称
4. googlePaperSpider.py--给定一篇paper，获得Googlescholar中的信息
5. tools用到的一些工具
	a. Crawl_proxy 爬取一些代理，用于对付反爬虫
	b. mysqlpool mysql连接池类
	c. 其他不再用了

6. mysalHandle 对mysql数据库表之间的处理数据以及存取操作

7. linux下部署依赖
	a. python 2.7.12
	b. scrapy 1.4.0
		安装scrapy之前
		sudo apt-get install build-essential libssl-dev libffi-dev python-dev libxml2-dev
		sudo pip install scrapy		
	c. mysqlpool DBUtils
		sudo pip install DBUtils
