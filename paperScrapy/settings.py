# -*- coding: utf-8 -*-

# Scrapy settings for paperScrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html


BOT_NAME = 'paperScrapy'

SPIDER_MODULES = ['paperScrapy.spiders']
NEWSPIDER_MODULE = 'paperScrapy.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'paperScrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True


# Mysql数据库的配置信息
MYSQL_HOST = '192.168.1.198'
MYSQL_DBNAME = 'citation_raw_qian'           # 数据库名字，请修改
MYSQL_USER = 'jingshuai'            # 数据库账号，请修改
MYSQL_PASSWD = '123456'             # 数据库密码，请修改

MYSQL_PORT = 3306                   # 数据库端口，在dbhelper中使用

# 爬虫出现Forbidden by robots.txt
ROBOTSTXT_OBEY = False

# 下载延迟反被封锁ip
CONCURRENT_REQUESTS = 8
DOWNLOAD_DELAY = 3.5

# 禁用cookies
# COOKIES_ENABLED = False
# COOKIES_DEBUG = True

# AUTOTHROTTLE_ENABLED = True
# AUTOTHROTTLE_START_DELAY = 1


# 配置代理
# DOWNLOADER_MIDDLEWARES = {
#  'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
#  'paperScrapy.middlewares.ProxyMiddleware': 100,
# }


# Configure item pipelinesn
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#     'paperScrapy.pipelines.PaperscrapyPipeline': 300,         # 保存到mysql数据库
#     # 'paperScrapy.pipelines.JsonWithEncodingPipeline': 300,    # 保存到文件中
# }


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'paperScrapy.middlewares.PaperscrapySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'paperScrapy.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'paperScrapy.pipelines.PaperscrapyPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
