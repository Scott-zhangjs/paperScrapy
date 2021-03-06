# -*- coding: utf-8 -*-
import hashlib
import random
import requests
from time import sleep

import scrapy
from scrapy.http import Request

from paperScrapy.items import GooglePaperItem
from paperScrapy.tools.mysqlpool import MysqlPool
from scrapy.http.cookies import CookieJar
from user_agent import generate_user_agent



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

        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, sdch, br',
		'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
		'Connection':'keep-alive',
		'Host':'xue.glgoo.org',
		'Referer':'https://xue.glgoo.org/scholar?hl=en&num=20&as_sdt=0',
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
		'Upgrade-insecure-requests': '1',
		# 'Cookie':'NID=102=pyCjX1MOSHvPDqPOZUIKBizmW0foKeaR3bJTv_D1-rPXp6lSngB_9hJlm3E8S_kh7JXmARV5L75mFAyZRxPNB755G_EQN5OQBliF2ED7SEIe_7Vkc_uRo7ZLL5O-5jDN; GSP=LM=1494141126:S=n66R0pUXuVXV-niY; Hm_lvt_6399b1342e7e174a203e2eb98d019207=1494141073; Hm_lpvt_6399b1342e7e174a203e2eb98d019207=1494141828',
    }

    # cookie = []



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

    # 计算成功的个数
    count = 0
    # url列表
    url = [
        # "https://scholar.google.com.hk",
        # "https://www.xichuan.pub",
        # "http://gg2.firstguo.com",
        "http://a3.zgdhhjha.com",
        "https://xue.glgoo.com",
        # "http://www.sci-hub.xyz",
        # "https://bb.qqmmgj.com",
        # "http://g.sci-hub.cn",
        # "https://g.zmirrordemo.com/extdomains/scholar.google.com",
        # "https://kuaiguge.co",
        # "https://google.speeder.cf/extdomains/scholar.google.com",
        # "https://c.ggkai.men/extdomains",
        # "https://e.ggkai.men/extdomains",
        # "https://d.ggkai.men/extdomains",
        # "http://c1.zgdhhjha.com",
        # "http://g2.zgdhhjha.com",
        # "http://g4.zgdhhjha.com",
    ]
    # 对应host列表
    host= [
        # "scholar.google.com.hk",
        # "www.xichuan.pub",
        # "gg2.firstguo.com",
        "a3.zgdhhjha.com",
        "xue.glgoo.com",
        # "www.sci-hub.xyz",
        # "bb.qqmmgj.com",
        # "g.sci-hub.cn",
        # "g.zmirrordemo.com",
        # "kuaiguge.co",
        # "google.speeder.cf",
        # "c.ggkai.men",
        # "e.ggkai.men",
        # "d.ggkai.men",
        # "c1.zgdhhjha.com",
        # "g2.zgdhhjha.com",
        # "g4.zgdhhjha.com",
    ]

    # myCookiejar = ''

    def getCookie(self):
        # fake google id (looks like it is a 16 elements hex)
        rand_str = str(random.random()).encode('utf8')
        google_id = hashlib.md5(rand_str).hexdigest()[:16]

        self.headers['Cookie'] = 'GSP=ID=%s' % google_id + ":CF=%d" % 4


    # 获取初始request
    def start_requests(self):

        for i in range(len(self.ccf_paper_set)):

            # 从CCF集合中取出
            paper_id = self.ccf_paper_set[i]["paper_id"]
            paper_title = self.ccf_paper_set[i]["paper_title"]
            paper_publicationYear = self.ccf_paper_set[i]["paper_publicationYear"]
            paper_publicationYear = str(paper_publicationYear)

            # url = "https://xue.glgoo.org/"    # 'http://202.168.155.123/' # "https://www.xichuan.pub/"
            # weizhui = '&btnG=&as_sdt=1%2C5&as_sdtp=&as_ylo=%d&as_yhi=%d' %(paper_publicationYear, paper_publicationYear)

            myUrl = i % len(self.url)
            self.headers['Host'] = self.host[myUrl]
            urlTitle = self.url[myUrl] + "/scholar?hl=en&q=" + str(paper_title.replace(":", "%3A") \
                        .replace("'", "%27").replace("&", "%26").replace("(", "%28") \
                        .replace(")", "%29").replace( "/", "%2F").replace(" ", "+")) \
                       + '+' + '&btnG=&as_sdtp=&as_ylo=' + paper_publicationYear \
                       + '&as_yhi=' + paper_publicationYear

            # 随机产生user-agent
            # self.headers['User-Agent'] = generate_user_agent()
            self.headers['Referer'] = urlTitle
            self.getCookie()


            # 通过meta传递参数venue_id、venue_type，方便后续的数据库存取
            # if i%10 == 0:
            # myJar = i % 20
            yield Request(urlTitle, headers=self.headers,
                          meta={'paper_id': paper_id, 'paper_title': paper_title},
                          callback=self.parse_googlePaper)
            # else:
            # yield Request(urlTitle, headers=self.headers,
            #               meta={'cookiejar': i, 'paper_id': paper_id, 'paper_title': paper_title},
            #               callback=self.parse_googlePaper)

            # print 'headers is ------->', self.headers
            # print 'mycookiejar is ------->', self.myCookiejar
            # if i > 0 and i % 100 == 0:
            #     print' 睡一会.(～﹃～)~zZ'
            #     sleep(random.uniform(10,15))

    def parse_googlePaper(self, response):
        """
        
        :param response: 
        :return: 
        """
        self.count += 1 # 计数
        print '成功的个数: ', self.count
        # self.myCookiejar = response.meta['cookiejar']

        paper_id = response.meta['paper_id']    # 从 meta取出变量paper_id
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



















