# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
# id	mind_map_node_alias	remark	title	text	web_category
class DmozItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    data = scrapy.Field()
    pages=scrapy.Field()
    current_page=scrapy.Field()
    # answer=scrapy.Field()
    # _id=scrapy.Field()
    # desc = scrapy.Field()


# class MihuaItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
