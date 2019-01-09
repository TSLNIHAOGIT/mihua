# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pandas as pd
class MihuaPipeline(object):
    def __init__(self):

        self.items = []
    def process_item(self, item, spider):
        print('item',item)
        self.items.extend(item['data'])
        print('self.items',self.items)
        if item['current_page']==item['pages']:
            df = pd.DataFrame(self.items)
            df.to_csv('/Users/ozintel/Downloads/Tsl_python_progect/local_ml/mihua/mihua/data/to_collect_order.csv',index=False)

        print('len(self.items)',len(self.items))
        # return item# 会在控制台输出原item数据，可以选择不写
