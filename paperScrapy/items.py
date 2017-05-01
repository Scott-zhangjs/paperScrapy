# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PaperscrapyItem(scrapy.Item):
    # define the fields for your item here like:

    name = scrapy.Field()       # dblp_name
    venue_id = scrapy.Field()     # venue_id
    venue_type = scrapy.Field()     # 记录venue属于哪一个数据表如 ccf, core
