# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pandas as pd
from mihua.items import DmozItem,DetailItem

#不同级别的pipeline是按照优先级从高到低，同一个item一次经过各个pipeline
#多个爬虫绑定对应的pipeline
class MihuaPipeline(object):
    def __init__(self):

        self.items = []
        self.my_order_detail_items=[]
    def process_item(self, item, spider):
        if spider.name == 'mihua':
            print('item',item)#item是一个字典
            self.items.extend(item['data'])
            print('self.items',self.items)
            if item['current_page']==item['pages']:
                df = pd.DataFrame(self.items)
                # df.to_csv('/Users/ozintel/Downloads/Tsl_python_progect/local_ml/mihua/mihua/data/to_collect_order.csv',index=False)
                df.to_excel('/Users/ozintel/Downloads/Tsl_python_progect/local_ml/mihua/mihua/data/to_collect_order.xlsx',
                          index=False)
            print('len(self.items)',len(self.items))
            # return item# 会在控制台输出原item数据，可以选择不写
        elif spider.name == 'mihua_post_data':

            if isinstance(item, DmozItem):
                print('my order item', item)
                self.items.extend(item['data'])
                print('len(self.items)', len(self.items))

                if item['current_page'] == item['pages'] :
                    print('准备保存my_order数据')
                    df = pd.DataFrame(self.items)
                    print('df.head',df.head())
                    df.to_excel(
                        '/Users/ozintel/Downloads/Tsl_python_progect/local_ml/mihua/mihua/data/my_order.xlsx',
                        index=False)







                    # df_my_order_and_detail = pd.merge(df, df_my_order_detail, how='inner',
                    #                                   left_on=['borrowName', 'borrowUserId'],
                    #                                   right_on=['detail_user_name', 'detail_user_id'])
                    # print('df_my_order_and_detail.head',df_my_order_and_detail.head())
                    #
                    # # df.to_csv('/Users/ozintel/Downloads/Tsl_python_progect/local_ml/mihua/mihua/data/to_collect_order.csv',index=False)
                    # df_my_order_and_detail.to_excel(
                    #     '/Users/ozintel/Downloads/Tsl_python_progect/local_ml/mihua/mihua/data/my_order_and_detail.xlsx',
                    #     index=False)
                # else:
                #     print('我的订单数据总数和处理中的数据总数不一致，出错')
            elif isinstance(item, DetailItem):
                print('post_data_item', item)  # item是一个字典
                each_person_my_order_detail={
                                           'import_name':item['import_name'],
                                           'import_contact':item['import_contact'],
                                           'import_relation':item['import_relation'],
                                           'other_name':item['other_name'],
                                           'other_contact':item['other_contact'],
                                           'other_relation':item['other_relation'],
                                           'detail_user_id':item['detail_user_id'] ,
                                           'detail_user_name':item['detail_user_name']
                }
                self.my_order_detail_items.append(each_person_my_order_detail)
                print('len(self.my_order_detail_items)', len(self.my_order_detail_items))

                if  item['total_data_counts'] == len(self.my_order_detail_items):
                    print('准备保存my_order_detail数据')
                    df_my_order_detail = pd.DataFrame(self.my_order_detail_items)
                    print('df_my_order_detail',df_my_order_detail.head())
                    df_my_order_detail.to_excel(
                        '/Users/ozintel/Downloads/Tsl_python_progect/local_ml/mihua/mihua/data/my_order_detail.xlsx',
                        index=False)
            else:
                print('出错，不属于任何已有的item')









            # return item

# class MihuaPipeline_post_data_spider(object):
#     def __init__(self):
#
#         self.items = []
#     def process_item(self, item, spider):
#         print('item',item)#item是一个字典
#         # self.items.extend(item['data'])
#         # print('self.items',self.items)
#         # if item['current_page']==item['pages']:
#         #     df = pd.DataFrame(self.items)
#         #     # df.to_csv('/Users/ozintel/Downloads/Tsl_python_progect/local_ml/mihua/mihua/data/to_collect_order.csv',index=False)
#         #     df.to_excel('/Users/ozintel/Downloads/Tsl_python_progect/local_ml/mihua/mihua/data/to_collect_order.xlsx',
#         #               index=False)
#         #
#         # print('len(self.items)',len(self.items))
#         # # return item# 会在控制台输出原item数据，可以选择不写