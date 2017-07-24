# -*- coding: utf-8 -*-
# @Time：
import re
from scrapy import cmdline

# from paperScrapy.tools.mysqlpool import MysqlPool
# from tools import mygscholar

# print mygscholar.query('artificial neural networks')


name = 'dblpSpider_conf'
cmd = 'scrapy crawl {0}'.format(name)
# cmd = cmd + ' -L WARNING'
print cmd
cmdline.execute(cmd.split())
#
# dbpool = MysqlPool()
# tmp = dbpool.getAll('select proxies_id from proxies')
# print type(tmp)
# print type(tmp[0])

# mypool = MysqlPool()
#
# # 查找targetpaper 中
# targetpaper_sql_select = "SELECT targetPaper_id, targetPaper_scholarTitle FROM targetpaper " \
#                          "WHERE targetPaper_dblp_name is NULL" \
#                          # "and targetPaper_id>1530000"
#
# targetpaper_set = mypool.getAll(targetpaper_sql_select)
# print 'first data is ', type(targetpaper_set)
# # 计数
# count = len(targetpaper_set)
# print 'the count is ', count
#
# for paper in targetpaper_set:
#
#     regexp = re.compile(r'[^\x00-\x7f]')
#     if regexp.search(paper['targetPaper_scholarTitle']):
#         print paper['targetPaper_scholarTitle']
#         count -= 1
#
# print 'the count is ', count