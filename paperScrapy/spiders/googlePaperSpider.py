# -*- coding: utf-8 -*-
import random
from time import sleep

import scrapy
from scrapy.http import Request

from paperScrapy.items import GooglePaperItem
from paperScrapy.tools.mysqlpool import MysqlPool


class GooglePaperSpider(scrapy.Spider):

    name = "googlePaperSpider"

    # 使用对应的pipline存储类
    custom_settings = {
        'ITEM_PIPELINES': {
            'paperScrapy.pipelines.GooglePaperPipeline': 1,
        }
    }

    headers = {
        #
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, sdch, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        # 'Connection':'keep-alive',
        # # 'Cookie': 'NID=101=kIp1iRvNwFTEwn3KxMxcNiN1u0tefKE88AAwv43RCRIq88DyjIUs7IBX-RMFT7JsGyS3MuojSSbK67M3G_vW8a7MM53pwebVFk5PWfTrid08rM57bHsKrezt8Xxd4Rf-; GSP=LM=1493962237:S=1xYoFQYMuCFUhMX1; Hm_lvt_0f47b9feac1b36431493d82d708e859a=1493962239; Hm_lpvt_0f47b9feac1b36431493d82d708e859a=1493962239',
        # 'Host': 'xichuan.pub',
        # 'Referer': 'https://xichuan.pub/scholar?hl=en&num=20&as_sdt=0%2C5',
        # # 'Upgrade-Insecure-Requests': '1',
        # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',

        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, sdch, br',
		'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
		# 'Connection':'keep-alive',
		'Host':'kuaiguge.co',
		'Referer':'https://kuaiguge.co/scholar?hl=en&num=20&as_sdt=0',
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
		'upgrade-insecure-requests': '1',
		# 'Cookie':'NID=102=qzJh3hVBvnFjJ1yWhKpZzv5jLQ99_eozfFFqWZZK0CLNQ4uoVscAIJw8kH_DqoQIgmvUonjFowLqdoui79I4QkSLyiIHfaVWBDewT85WwnH3tlVjSyneSbJPfdfUvY2C; GSP=NW=1:LM=1493992992:S=1LQyPfQ2WAG1xKPw; _ga=GA1.2.656936550.1493992987; _gid=GA1.2.605575076.1493992994',
    }

    cookie = []

    mypool = MysqlPool()  # 创建连接池

    # 查询ccf中为进行dblp匹配
    ccf_sql_select = "SELECT paper_id, paper_title, paper_publicationYear\
    				from paper, venue, dblp, dblp2ccf, ccf\
    				where dblp_id != '999999999' \
    				and venue_venue_id = venue_id \
    				and venue.dblp_dblp_id = dblp_id \
    				and dblp_id = dblp2ccf.dblp_dblp_id \
    				and ccf_CCF_id = CCF_id\
    				and CCF_classification = %s\
    				and CCF_type = %s\
    				and paper_nbCitation = -1"

    ccf_paper_set = mypool.getAll(ccf_sql_select, ("A", "Conference"))  # 记录所有待查询的venue集合

    # 获取初始request
    def start_requests(self):

        for i in range(len(self.ccf_paper_set)):

            # 从CCF集合中取出
            paper_id = self.ccf_paper_set[i]["paper_id"]
            paper_title = self.ccf_paper_set[i]["paper_title"]
            paper_publicationYear = self.ccf_paper_set[i]["paper_publicationYear"]
            paper_publicationYear = str(paper_publicationYear)

            url = "https://kuaiguge.co/"    # 'http://202.168.155.123/' # "https://www.xichuan.pub/"
            # weizhui = '&btnG=&as_sdt=1%2C5&as_sdtp=&as_ylo=%d&as_yhi=%d' %(paper_publicationYear, paper_publicationYear)
            urlTitle = url + "scholar?hl=en&q=" + str(paper_title.replace(":", "%3A") \
                        .replace("'", "%27").replace("&", "%26").replace("(", "%28") \
                        .replace(")", "%29").replace( "/", "%2F").replace(" ", "+")) \
                       + '+' + '&btnG=&as_sdtp=&as_ylo=' + paper_publicationYear \
                       + '&as_yhi=' + paper_publicationYear

            # 通过meta传递参数venue_id、venue_type，方便后续的数据库存取

            # self.headers['Cookie'] = random.choice(self.cookie)
            yield Request(urlTitle, headers=self.headers,
                          meta={'paper_id': paper_id, 'paper_title': paper_title},
                          callback=self.parse_googlePaper)
            if i%100 == 0:
                sleep(random.uniform(8,10))
                print '睡一会........................................'

        # paper_id = '1'
        # paper_title = "Technology for developing regions: Moore's law is not enough"
        # paper_title = "Smart packets: applying active networks to network management"
        # paper_publicationYear = '2000'
        # url = "https://www.xichuan.pub/"
        # # weizhui = '&btnG=&as_sdt=1%2C5&as_sdtp=&as_ylo=%d&as_yhi=%d' %(paper_publicationYear, paper_publicationYear)
        # urlTitle = url + "scholar?hl=en&q=" + str(paper_title.replace(":", "%3A") \
        #                                           .replace("'", "%27").replace("&", "%26").replace("(", "%28") \
        #                                           .replace(")", "%29").replace("/", "%2F").replace(" ", "+")) \
        #             + '&btnG=&as_sdtp=&as_ylo=' + paper_publicationYear \
        #            + '&as_yhi=' + paper_publicationYear
        #
        # # 通过meta传递参数venue_id、venue_type，方便后续的数据库存取
        # yield Request(urlTitle, headers=self.headers,
        #               meta={'paper_id': paper_id, 'paper_title': paper_title},
        #               callback=self.parse_googlePaper)


    def parse_googlePaper(self, response):
        """
        
        :param response: 
        :return: 
        """
        paper_id = response.meta['paper_id']  # 从meta取出变量paper_id
        paper_title = response.meta['paper_title']  # 从meta取出变量paper_id
        print 'parse_googlePaper: paper_id', paper_id

        try:


            # 获取当前的内容块
            cur_box = response.xpath('//*[@id="gs_ccl_results"]/div[1]')
            ccl_results = cur_box.xpath('.//div[@class="gs_ri"]/h3/a//text()').extract()
            ccl_results = ''.join(ccl_results)
            print 'ccl_results:', ccl_results

            # 比较是否是自己要找的
            paper_title_tmp = filter(str.isalpha, paper_title).lower()
            cur_title_tmp = filter(str.isalpha, str(ccl_results)).lower()

            if paper_title_tmp != cur_title_tmp:    # 未找到时抛出异常
                raise Exception("The two papers are different!\nCurrent: '%s'\nOrigin: '%s'"%(ccl_results, paper_title))

            # 开始分析各个字段
            # 引用数目和链接
            paper_nbCitation = cur_box.xpath('.//div[@class="gs_fl"]/a[1]//text()').extract()
            paper_nbCitation = ''.join(paper_nbCitation)
            if 'Cited by' not in paper_nbCitation:
                paper_nbCitation = 0
                paper_citationURL = ""
            else:
                paper_nbCitation = int(paper_nbCitation.replace('Cited by', '').strip())
                paper_citationURL = cur_box.xpath('.//div[@class="gs_fl"]/a[1]/@href').extract()[0]

            # 题目链接
            paper_rawURL = cur_box.xpath('.//div[@class="gs_ri"]/h3/a/@href').extract()
            paper_rawURL = "".join(paper_rawURL)

            # 论文paf链接
            paper_isseen = cur_box.xpath('.//span[@class="gs_ctg2"]/text()').extract()
            if len(paper_isseen) == 0 or 'PDF' not in paper_isseen[0]:
                paper_isseen = 0
                paper_pdfURL = ""
            else:
                paper_isseen = 1
                paper_pdfURL = cur_box.xpath('.//div[@class="gs_ggsd"]/a[1]/@href').extract()[0]

            # 论文信息
            paper_scholarInfo = cur_box.xpath('.//div[@class="gs_a"]//text()').extract()
            paper_scholarInfo = "".join(paper_scholarInfo)

            # 摘要
            paper_rawInfo =  cur_box.xpath('.//div[@class="gs_rs"]//text()').extract()
            paper_rawInfo = "".join(paper_rawInfo)

            # 相关论文链接
            paper_relatedURL = cur_box.xpath('.//a[text()="Related articles"]/@href').extract()
            paper_relatedURL = "".join(paper_relatedURL)

            print '------------------爬取信息展示-----------------------'
            print 'paper_nbCitation', paper_nbCitation
            print 'paper_citationURL', paper_citationURL
            print 'paper_rawURL', paper_rawURL
            print 'paper_isseen', paper_isseen
            print 'paper_pdfURL', paper_pdfURL
            print 'paper_scholarInfo', paper_scholarInfo
            print 'paper_rawInfo', paper_rawInfo
            print 'paper_relatedURL', paper_relatedURL

            item = GooglePaperItem()
            item['paper_id'] = paper_id
            item['paper_nbCitation'] = paper_nbCitation
            item['paper_citationURL'] = paper_citationURL
            item['paper_rawURL'] = paper_rawURL
            item['paper_isseen'] = paper_isseen
            item['paper_pdfURL'] = paper_pdfURL
            item['paper_scholarInfo'] = paper_scholarInfo
            item['paper_rawInfo'] = paper_rawInfo
            item['paper_relatedURL'] = paper_relatedURL

            yield item

        except Exception, e:        # 匹配到多个或者没匹配到
            print e.args[0]

            item = GooglePaperItem()
            item['paper_id'] = paper_id
            item['paper_nbCitation'] = -2
            item['paper_citationURL'] = ""
            item['paper_rawURL'] = ""
            item['paper_isseen'] = -2
            item['paper_pdfURL'] = ""
            item['paper_scholarInfo'] = ""
            item['paper_rawInfo'] = ""
            item['paper_relatedURL'] = ""

            yield item
            # print 'venue_url',venue_url
        # item = PaperscrapyItem()
        #
        # yield item

















