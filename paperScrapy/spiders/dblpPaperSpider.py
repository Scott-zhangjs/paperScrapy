# # -*- coding: utf-8 -*-
# from time import sleep
#
# import scrapy
# from scrapy.http import Request
#
#
# # import urllib2
# from paperScrapy.items import PaperscrapyItem, PaperDBLPItem
# from paperScrapy.tools.mysqlpool import MysqlPool
# from user_agent import generate_user_agent
#
#
# class DblpPaperSpider(scrapy.Spider):
#
#     name = "dblpPaperSpider"
#
#     # 使用对应的pipline存储类
#     custom_settings = {
#         'ITEM_PIPELINES': {
#             'paperScrapy.pipelines.DblpPaperPipeline': 1,
#         }
#     }
#
#     headers = {
#         'Host': 'dblp.uni-trier.de',
#         # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
#         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
#         'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
#         'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
#         'Accept-Encoding': 'gzip, deflate, sdch',
#         'Referer': 'http://dblp.uni-trier.de/',
#         'Cookie': 'dblp-hideable-show-feeds=true; dblp-hideable-show-rawdata=true; dblp-view=y; dblp-search-mode=c',
#         # 'Cookie': 'dblp-view=y; dblp-search-mode=c',
#         'Connection': 'keep-alive',
#         'Cache-Control': 'max-age=0',
#     }
#
#
#     mypool = MysqlPool()  # 创建连接池
#
#
#     # 查找targetpaper 中
#     targetpaper_sql_select = "SELECT targetPaper_id, targetPaper_scholarTitle FROM targetpaper " \
#                              "WHERE targetPaper_dblp_name is NULL " \
#                              # "and targetPaper_id>=2100000 and targetPaper_id>1530000"
#
#     targetpaper_set = mypool.getAll(targetpaper_sql_select)
#     print 'first data is ', targetpaper_set[0]
#     # 计数
#     count = len(targetpaper_set)
#     print 'the count is ', count
#
#     # 获取初始request
#     def start_requests(self):
#         tmpurl = [
#             "http://dblp.uni-trier.de/search?q=",
#             "http://dblp.org/search?q="
#         ]
#         tmphost = [
#             "dblp.uni-trier.de",
#             "dblp.org"
#         ]
#
#         tmpreferer = [
#             "http://dblp.uni-trier.de",
#             "http://dblp.org"
#         ]
#
#         for i in range(len(self.targetpaper_set)):
#         # for i in range(100):
#         # i = 0
#         # if i == 0 :
#             paper_title = self.targetpaper_set[i]["targetPaper_scholarTitle"]
#             paper_id = self.targetpaper_set[i]["targetPaper_id"]
#             line = paper_title.replace("%", "%25").replace(" ", "%20").replace(",", "%2C")\
#                 .replace(":", "%3A").replace("?", "%3F").replace("&", "%26").replace("'", "%27")
#             url = tmpurl[i % 2] + line
#             self.headers['Host'] = tmphost[i % 2]
#             self.headers['Referer'] = tmpreferer[i % 2]
#             self.headers['User-Agent'] = generate_user_agent()
#             # url = 'http://dblp.uni-trier.de/search?q=' + line
#             # print 'the url is', url
#             # print 'the user agent is', self.headers['User-Agent']
#
#             yield Request(url, headers=self.headers,
#                           meta={'paper_id': paper_id}, callback=self.parse_paper_url)
#             # print 'the user agent is', self.headers['User-Agent']
#         #
#         #     # sleep(2)        #休眠
#
#     # 暂未使用
#     def parse(self, response):
#         item = PaperscrapyItem()    # 声明自己定义的item类
#         yield item
#
#
#     def parse_paper_url(self, response):
#         """
#         解析找到论文的dblp名称
#         :param response: 一篇paper所产生的请求的响应
#         :return: 对一篇论文的dblp名字
#         """
#         paper_id = response.meta['paper_id']  # 从meta取出变量paper_id
#         try:
#
#             # 找到匹配到的href
#             dblp_year = response.xpath('//ul[@class="publ-list"]/li[1]/text()').extract()
#             # print dblp_year
#             dblp_name = response.xpath('//ul[@class="publ-list"]/li[2]/div[@class="data"]/a/span[1]/span/text()').extract()
#             dblp_num = len(dblp_name)
#             if dblp_num == 0:
#                 raise Exception("Not matches paper!")
#             elif dblp_num > 1:
#                 raise Exception("Too many matches paper!")
#
#             dblp_year = dblp_year[0]
#             dblp_name = dblp_name[0]
#
#         except Exception, e:        # 匹配到多个或者没匹配到
#             print e.args[0]
#             print 'dblp_name', dblp_name
#             dblp_name = 'NOT IN DBLP'
#             dblp_year = -1
#
#         paper_item = PaperDBLPItem()  # 声明自己定义的item类 并赋值
#         paper_item['name'] = dblp_name
#         paper_item['year'] = dblp_year
#         paper_item['paper_id'] = paper_id
#
#
#         print '---------show info--------'
#         print 'paper id:', paper_id
#         print 'year:', dblp_year
#         print 'name:', dblp_name
#
#         yield paper_item
#
#         self.count = self.count - 1
#         print '---------remain--------', self.count
#
