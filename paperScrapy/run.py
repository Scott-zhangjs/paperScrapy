# -*- coding: utf-8 -*-
# @Time：

from scrapy import cmdline

from paperScrapy.tools.mysqlpool import MysqlPool
# from tools import mygscholar

# print mygscholar.query('artificial neural networks')


name = 'dblpPaperSpider'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
#
# dbpool = MysqlPool()
# tmp = dbpool.getAll('select proxies_id from proxies')
# print type(tmp)
# print type(tmp[0])