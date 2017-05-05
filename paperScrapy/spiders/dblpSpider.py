# -*- coding: utf-8 -*-
from time import sleep

import scrapy
from scrapy.http import Request

from paperScrapy.items import PaperscrapyItem
from paperScrapy.tools.mysqlpool import MysqlPool


class DblpSpider(scrapy.Spider):

    name = "dblpSpider"

    # 使用对应的pipline存储类
    custom_settings = {
        'ITEM_PIPELINES': {
            'paperScrapy.pipelines.DblpPipeline': 1,
        }
    }

    # headers = {
    #     'Host': 'dblp.uni-trier.de',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #     'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    #     'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    #     'Accept-Encoding': 'gzip, deflate, sdch',
    #     'Referer': 'http://dblp.uni-trier.de/',
    #     'Cookie': 'dblp-hideable-show-feeds=true; dblp-hideable-show-rawdata=true; dblp-view=y; dblp-search-mode=c',
    #     'Connection': 'keep-alive',
    #     'Cache-Control': 'max-age=0',
    # }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    mypool = MysqlPool()  # 创建连接池

    # 查询ccf中为进行dblp匹配
    ccf_sql_select = "SELECT CCF_id, CCF_name " \
                 "FROM ccf WHERE CCF_id<10000000 AND CCF_dblpname = %s and CCF_type = 'journal'"

    ccf_venue_set = mypool.getAll(ccf_sql_select, ("NOT IN DBLP",))  # 记录所有待查询的venue集合

    #  查询core中为进行dblp匹配
    core_sql_select = "SELECT CORE_id, CORE_name " \
                 "FROM core WHERE CORE_id<10000000 AND CORE_dblpname = %s and CORE_type = 'journal'"

    core_venue_set = mypool.getAll(core_sql_select, ("NOT IN DBLP",))  # 记录所有待查询的venue集合

    # 获取初始request
    def start_requests(self):

        # # 更新会议
        # conference_select = "SELECT CCF_id, CCF_abbreviation " \
        #              "FROM ccf WHERE CCF_id<10000000 AND CCF_dblpname = %s and CCF_type = 'conference'"
        #
        # conference_set = self.mypool.getAll(conference_select, ("NOT IN DBLP",))  # 记录所有待查询的venue集合
        # for con in conference_set:
        #
        #     con_id = con["CCF_id"]
        #     con_abb= con["CCF_abbreviation"]
        #     update_sql = "update ccf set CCF_dblpname = %s where CCF_id = %s "
        #     self.mypool.update(update_sql, (con_abb, con_id))
        # self.mypool.end()
        # print 'Conference is updated successful!'
        #


        # for i in range(len(self.ccf_venue_set)):
        #
        #     # 从CCF集合中取出
        #     venue_name = self.ccf_venue_set[i]["CCF_name"]
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
    # 暂未使用
    def parse(self, response):
        item = PaperscrapyItem()    # 声明自己定义的item类
        yield item



    def parse_venue(self, response):
        """
        找到匹配到的期刊
        :param response: 输入期刊后得到的响应
        :return: 发起对期刊的请求
        """
        try:
            venue_id = response.meta['venue_id']    # 从meta取出变量venue_id
            venue_type = response.meta['venue_type']    # 从meta取出变量venue_type
            print 'parse_venue: venue_id', venue_id
            # 找到匹配到的href
            venue_ul = response.xpath('//div[@id="completesearch-venues"]/div/ul')  # 区分开exact和likely matches

            if len(venue_ul) == 0:
                raise Exception("No matches!")

            venue_url = venue_ul[0].xpath('.//li/a/@href').extract()
            href_num = len(venue_url)

            matches_type = response.xpath('//*[@id="completesearch-venues"]/div/p[1]/text()').extract()

            # print 'the type is ', matches_type[0], 'the num of venue', href_num

            paper_type = 'journal'
            if href_num > 2:    # url多于两个，判定为连接过多
                raise Exception("Too many matches venue!")
            elif href_num == 2:     # 两个链接中去带有journals
                # 首先判断匹配类型
                if matches_type[0] != 'Exact matches':
                    raise Exception("Too many matches venue!")

                if paper_type not in venue_url[0] and paper_type not in venue_url[1]:
                    raise Exception("Not matches venue!")
                # 关于两个都journal的情况，是认为匹配过多还是都满足呢？
                # if paper_type in venue_url[0] and paper_type in venue_url[1]:
                #     raise Exception("Too many matches venue!")
                # 把带有journal的链接付给第一个url
                if paper_type not in venue_url[0]:
                    venue_url[0] = venue_url[1]

            elif href_num == 1:
                if paper_type not in venue_url[0]:
                    raise Exception("Not matches venue!")

        except Exception, e:        # 匹配到多个或者没匹配到
            print e.args[0]
            # print 'venue_url',venue_url
        else:

            print 'venue_url', venue_url[0]
            # 对匹配到的venue继续请求
            # sleep(1)  # 休眠
            yield Request(venue_url[0], headers=self.headers,
                          meta={'venue_id': venue_id, 'venue_type': venue_type}, callback=self.parse_volume)

    def parse_volume(self, response):
        """
        找到volumes
        :param response: 从期刊处得到链接产生的请求结果
        :return: 对每一个名字（最多三个）所对应的volume发起一个请求
        """
        try:
            venue_id = response.meta['venue_id']    # 从meta取出变量venue_id
            venue_type = response.meta['venue_type']  # 从meta取出变量venue_type
            print 'parse_volume: venue_id', venue_id

            # 找到匹配到不同名称的venue
            volume_ul = response.xpath('//*[@id="main"]/ul')
            volume_url = []
            # 解析venue下的volume
            for vul in volume_ul:
                tmp = vul.xpath('.//li/a[1]/@href').extract()
                # print 'tmp------',tmp
                if len(tmp) != 0:
                    volume_url.append(tmp[0])
            href_num = len(volume_url)      # 匹配到链接的个数
            print 'parse_volume: ', href_num
            if href_num == 0:
                raise Exception("Not matches volume!")
        except Exception, e:        # 匹配到多个或者没匹配到
            print e.args[0]
            print 'volume_url',volume_url
        else:
            print 'run volume_url', volume_url
            # 对匹配到前3个url进行请求
            tmp = (href_num if href_num<3 else 3)   # 在href_num 和 3 中找到较小数
            for i in range(tmp):
                # sleep(1)  # 休眠
                yield Request(volume_url[i], headers=self.headers,
                              meta={'venue_id': venue_id, 'venue_type': venue_type}, callback=self.parse_paper)

    def parse_paper(self, response):
        """
        找到分享处的链接
        :param response: 一个volume发起请求的响应
        :return: 对一篇论文的请求
        """

        try:
            venue_id = response.meta['venue_id']    # 从meta取出变量venue_id
            venue_type = response.meta['venue_type']  # 从meta取出变量venue_type
            print 'parse_paper: venue_id', venue_id
            # 找到匹配到的href
            paper_url = response.xpath('//*[@class="select-on-click"]/small/text()').extract()
            href_num = len(paper_url)
            if href_num == 0:
                raise Exception("Not matches paper!")
        except Exception, e:        # 匹配到多个或者没匹配到
            print e.args[0]
            print 'paper_url',paper_url
        else:
            # print 'paper_url', paper_url[1]
            # 对匹配到一篇论文请求
            # sleep(1)  # 休眠
            yield Request(paper_url[1], headers=self.headers,
                          meta={'venue_id': venue_id, 'venue_type': venue_type}, callback=self.parse_paper_url)



    def parse_paper_url(self, response):
        """
        解析找到论文的dblp名称
        :param response: 一篇paper所产生的请求的响应
        :return: 对一篇论文的dblp名字
        """

        try:
            venue_id = response.meta['venue_id']    # 从meta取出变量venue_id
            venue_type = response.meta['venue_type']  # 从meta取出变量venue_type
            print 'parse_paper_url: venue_id', venue_id
            # 找到匹配到的href
            dblp_name = response.xpath('//ul[@class="publ-list"]/li/div[@class="data"]/a/span[1]/span/text()').extract()
            dblp_num = len(dblp_name)
            if dblp_num == 0:
                raise Exception("Not matches paper!")
            elif dblp_num > 1:
                raise Exception("Too many matches paper!")
        except Exception, e:        # 匹配到多个或者没匹配到
            print e.args[0]
            print 'dblp_name', dblp_name
        else:
            # print 'dblp_name', dblp_name[0]

            paper_item = PaperscrapyItem()  # 声明自己定义的item类 并赋值
            paper_item['name'] = dblp_name[0]
            paper_item['venue_id'] = venue_id
            paper_item['venue_type'] = venue_type
            yield paper_item














