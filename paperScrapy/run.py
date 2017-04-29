# -*- coding: utf-8 -*-
# @Time：

from scrapy import cmdline


name = 'dblpSpider'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())