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



class GooglePaperItem(scrapy.Item):
    # define the fields for your item here like:

    paper_id = scrapy.Field()       # 引用量
    paper_nbCitation = scrapy.Field()       # 引用量
    paper_isseen = scrapy.Field()           # 是否有pdf
    paper_citationURL = scrapy.Field()      # 引用链接
    paper_pdfURL = scrapy.Field()           # pdf链接
    paper_scholarInfo = scrapy.Field()      # 论文信息
    paper_rawInfo = scrapy.Field()          # 摘要
    paper_rawURL = scrapy.Field()           # 原始链接
    paper_relatedURL = scrapy.Field()       # 相关论文链接