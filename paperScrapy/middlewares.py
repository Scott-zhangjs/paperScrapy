# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os

import time
from scrapy import signals

# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import base64
import random


# Start your middleware class
class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):

        '''对request对象加上proxy'''
        proxy = self.get_random_proxy()
        print "this is request ip:" + proxy
        request.meta['proxy'] = proxy


    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            proxy = self.get_random_proxy()
            print("this is response ip:" + proxy)
            # 对当前reque加上代理
            request.meta['proxy'] = proxy
            return request
        return response


    def get_random_proxy(self):
        '''随机从文件中读取proxy'''
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        dir = os.path.join(BASE_DIR, 'tools/proxies.txt')
        # print 'dir', dir
        proxyFile = open(dir)

        proxies = []

        for line in proxyFile:
            tmp = line.split(':')
            if tmp[0] == 'http':        # 专门挑选http，由于链接是http的
                proxies.append(str(line).replace("\n", ""))

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
