# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os

import time
from scrapy import signals
from scrapy.http.cookies import CookieJar

# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import base64
import random

# Start your middleware class
from paperScrapy.tools.Crawl_proxy import Proxies
from user_agent import generate_user_agent


class ProxyMiddleware(object):

    cproxy = Proxies()
    # the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

    count = 0
    cookie = {}
    # overwrite process request
    def process_request(self, request, spider):

        '''对request对象加上proxy'''

        # proxy = self.get_random_proxy()
        if 'https' in str(request.url.split(":")[0]):
            # print 'request.url.......', request.url
            proxy = self.cproxy.get_random_proxy_https()
        else:
            proxy = self.cproxy.get_random_proxy_http()
        print "this is request ip:" + proxy
        request.meta['proxy'] = proxy

        # 这句话用于随机选择user-agent
        # ua = random.choice(self.user_agent_list)
        ua = generate_user_agent()
        if ua:
            request.headers.setdefault('User-Agent', ua)

        # # 添加cookie
        # # print 'the cookie list is :', self.cookie
        # host_tmp = str(request.headers["Host"])
        # print 'the count is -->', self.count, 'the host is --------------------------->', host_tmp
        # cur_cookie = []
        # # print 'the count is -->', self.count, 'the current cookie dic is ------------->', self.cookie
        # if self.cookie.has_key(host_tmp):
        #     cur_cookie = self.cookie[host_tmp]
        # print 'the count is -->', self.count, 'the length of cookie is -------------------------->', len(cur_cookie)
        # print 'the count is -->', self.count, 'the header is ------------------------->', request.headers
        # if len(cur_cookie) > 0:
        #     request.headers['Cookie'] = random.choice(cur_cookie)
        #
        #     print 'the count is -->', self.count, 'the new header is ------------------>', request.headers
        #
        # # 定时清空cookie
        #
        # self.count += 1
        #
        # if self.count > 100:
        #     print '----------------500次了,清空cookie啦----------------'
        #     self.cookie = {}
        #     self.count = 0






    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            # proxy = self.get_random_proxy()
            if 'https' in str(request.url.split(":")[0]):
                # print 'request.url.......', request.url
                proxy = self.cproxy.get_random_proxy_https()
            else:
                proxy = self.cproxy.get_random_proxy_http()
            print("this is response ip:" + proxy)
            # 对当前reque加上代理
            request.meta['proxy'] = proxy
            return request

        # 处理cookies

        # if len(self.cookie) < 50:

        self.get_cookie(request, response)

        return response

    def get_cookie(self, request, response):
        # Referer_tmp =  headers['Referer']
        # url = "http://g.sci-hub.cn/scholar"
        # headers['User-Agent'] = generate_user_agent()
        # headers['Referer'] = 'http://dir.scmor.com/google/'
        try:
            if response.status != 200:
                raise Exception('---------当前未连接成功!--------------')
            # 更换Cookie，重置headers
            cookie_list = response.headers.getlist('Set-Cookie')    # 为cookie属性与值的字典
            print 'the count is -->',self.count, 'cookie_dic--------->', cookie_list
            try:
                cookie_NID = cookie_list[0].split(';')[0]
                cookie_GSP = cookie_list[1].split(';')[0]
                cookie = cookie_NID + "; " + cookie_GSP
                # 为对应host添加cookie
                host_tmp = str(request.headers["Host"])
                self.cookie.setdefault(host_tmp, []).append(cookie)
                print 'the count is -->',self.count, "CURRENT COOKIE: ----->" + cookie
            except:
                print 'the count is -->',self.count, "---GET cookie FAILED!----"
        except Exception, e:
            print e.args[0]



    def get_random_proxy(self):
        '''随机从文件中读取proxy'''
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        # dir = os.path.join(BASE_DIR, 'tools/httpsProxy.txt')
        # proxyFile = open(dir)
        # proxies = []
        #
        # for line in proxyFile:
        #
        #     proxies.append('https://' + str(line).replace("\n", ""))
        #
        #
        dir = os.path.join(BASE_DIR, 'tools/proxies.txt')
        # print 'dir', dir
        proxyFile = open(dir)

        proxies = []

        for line in proxyFile:
            tmp = line.split(':')
            if tmp[0] == 'http':        # 专门挑选http，由于链接是http的
                proxies.append(str(line).replace("\n", ""))
        # print 'proxies', proxies
        proxy = random.choice(proxies).strip()
        return proxy



class PaperscrapySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
