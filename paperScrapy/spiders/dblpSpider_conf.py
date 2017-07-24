# -*- coding: utf-8 -*-
from time import sleep

import scrapy
from scrapy.http import Request

from paperScrapy.items import PaperscrapyItem
from paperScrapy.tools.mysqlpool import MysqlPool

import re


class DblpSpider(scrapy.Spider):

    name = "dblpSpider_conf"

    # 使用对应的pipline存储类
    custom_settings = {
        'ITEM_PIPELINES': {
            'paperScrapy.pipelines.DblpPipeline': 1,
        }
    }

    headers = {
        'Host': 'dblp.uni-trier.de',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Referer': 'http://dblp.uni-trier.de/',
        'Cookie': 'dblp-hideable-show-feeds=true; dblp-hideable-show-rawdata=true; dblp-view=y; dblp-search-mode=c',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    }

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    # }

    mypool = MysqlPool()  # 创建连接池

    # 查询ccf中为进行dblp匹配
    ccf_sql_select = "SELECT CCF_id, CCF_name, CCF_abbreviation " \
                 "FROM ccf WHERE CCF_id<10000000 AND CCF_dblpname = %s and CCF_type = 'conference'"

    ccf_venue_set = mypool.getAll(ccf_sql_select, ("NOT IN DBLP",))  # 记录所有待查询的venue集合

    #  查询core中为进行dblp匹配
    core_sql_select = "SELECT CORE_id, CORE_name, CORE_abbreviation " \
                 "FROM core WHERE CORE_id<10000000 AND CORE_dblpname = %s and CORE_type = 'conference'"

    core_venue_set = mypool.getAll(core_sql_select, ("NOT IN DBLP",))  # 记录所有待查询的venue集合

    # 获取初始request
    def start_requests(self):


        # for i in range(len(self.ccf_venue_set)):
        #
        #     # 从CCF集合中取出
        #     #venue_name = self.ccf_venue_set[i]["CCF_name"]
        #     venue_name = self.ccf_venue_set[i]["CCF_abbreviation"]
        #     venue_id = self.ccf_venue_set[i]["CCF_id"]
        #     line = venue_name.replace("%", "%25").replace(" ", "%20").replace(",", "%2C")\
        #         .replace(":", "%3A").replace("?", "%3F").replace("&", "%26").replace("'", "%27")
        #     url = 'http://dblp.uni-trier.de/search?q=' + line
        #
        #     # 通过meta传递参数venue_id、venue_type，方便后续的数据库存取
        #     venue_type = 'CCF'
        #     yield Request(url, headers=self.headers,
        #                   meta={'venue_id': venue_id, 'venue_type': venue_type},
        #                   callback=self.parse_venue)
        #     sleep(2)        #休眠

        for i in range(len(self.core_venue_set)):
            # 从Core集合中取出
            venue_name = self.core_venue_set[i]["CORE_name"]
            # venue_name = self.ccf_venue_set[i]["CCF_abbreviation"]
            venue_id = self.core_venue_set[i]["CORE_id"]
            line = venue_name.replace("%", "%25").replace(" ", "%20").replace(",", "%2C")\
                .replace(":", "%3A").replace("?", "%3F").replace("&", "%26").replace("'", "%27")
            url = 'http://dblp.uni-trier.de/search?q=' + line

            # 通过meta传递参数venue_id、venue_type，方便后续的数据库存取
            venue_type = 'CORE'
            yield Request(url, headers=self.headers,
                          meta={'venue_id': venue_id, 'venue_type': venue_type}, callback=self.parse_venue)
        #
        #     # sleep(2)        #休眠

    def parse_venue(self, response):
        """
        找到匹配到的期刊
        :param response: 输入期刊后得到的响应
        :return: 发起对期刊的请求
        """
        try:
            venue_id = response.meta['venue_id']    # 从meta取出变量venue_id
            venue_type = response.meta['venue_type']    # 从meta取出变量venue_type
            dblp_name = 'NOT IN DBLP'
            print 'parse_venue: venue_id', venue_id

            # 找到结果ul块
            venue_ul = response.xpath('//div[@id="completesearch-venues"]/div/ul')  # 区分开exact和likely matches
            if len(venue_ul) == 0:
                raise Exception("No matches!")

            # 找到匹配到的href
            venue_url = venue_ul[0].xpath('.//li/a/@href').extract()

            matches_type = response.xpath('//*[@id="completesearch-venues"]/div/p[1]/text()').extract()
            # matches_name = venue_ul[0].xpath('.//li[1]/a/text()').extract()
            # //*[@id="completesearch-venues"]/div/ul/li/a/text()
            # print 'matches_name', matches_name
            # tmp_name = re.match(".*\((.*)\).*", matches_name[-1]).group(1)
            # print 'tmp_name:', tmp_name

            print 'the original url list is ', venue_url
            # 获取conf的链接
            conf_url = set()
            paper_type = 'conf'
            for vurl in venue_url:
                if paper_type in vurl:
                    conf_url.add(vurl)

            # 筛选名称
            conf_url = list(conf_url)
            print 'the new url list is ', conf_url
            conf_num = len(conf_url)
            if conf_num == 0:
                raise Exception("No matches conference!")
            elif conf_num == 1:
                tmp_name = conf_url[0].split('/')[-2]
                dblp_name = tmp_name.upper()
            else:
                dblp_name = 'MORE'
                if matches_type[0] == 'Exact matches':
                    raise Exception("Too many matches in exact matches!")
                else:
                    raise Exception("Too many matches in likely matches!")

        except Exception, e:        # 匹配到多个或者没匹配到
            print e.args[0]
            # yield Request(venue_url[0], headers=self.headers,
            #               meta={'venue_id': venue_id, 'venue_type': venue_type},
            #               callback=self.parse_short)
            # print 'venue_url',venue_url
        # else:
        paper_item = PaperscrapyItem()  # 声明自己定义的item类 并赋值
        print 'dblp_name is', dblp_name
        paper_item['name'] = dblp_name
        paper_item['venue_id'] = venue_id
        paper_item['venue_type'] = venue_type
        yield paper_item






