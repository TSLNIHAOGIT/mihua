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
    total_data_counts = scrapy.Field()







class DetailItem(scrapy.Item):
    import_name = scrapy.Field()
    other_name = scrapy.Field()
    import_contact = scrapy.Field()
    other_contact = scrapy.Field()
    import_relation = scrapy.Field()
    other_relation = scrapy.Field()
    detail_user_id = scrapy.Field()
    detail_user_name = scrapy.Field()
    total_data_counts = scrapy.Field()







# class MihuaItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
