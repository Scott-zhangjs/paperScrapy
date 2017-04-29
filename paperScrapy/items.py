# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PaperscrapyItem(scrapy.Item):
    # define the fields for your item here like:

    name = scrapy.Field()   # dblp_name
    # name1 = scrapy.Field()   # dblp_name1
    # name2 = scrapy.Field()   # dblp_name2
    venue_id = scrapy.Field()     # venue_id
