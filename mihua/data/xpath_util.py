import json
from scrapy.selector import Selector
'''content'''

path='/Users/ozintel/Downloads/Tsl_python_progect/local_ml/mihua/mihua/data/report_data_2.html'
import pandas as pd

body = '<body><span>good</span></body>'
res_body=Selector(text=body).xpath('//span/text()').extract()
print('res_body',res_body)


with open(path, 'r') as f:
    data = json.load(f)
    print(data)
    html_text=data['result']
    #取第6张表格的内容,td中的第一个

    res0 = Selector(text=html_text).xpath(
        # '//div[@class="table"][6]/div[@class="tabbox"]/table/tbody/tr[@class="center"]'


        # #正确方法
        '''//div[@class="table"][6]/div[@class="tabbox"]/table/tbody/tr[@class="center"][position()<4]/td[position()<3]/text()|
        //div[@class="table"][6]/div[@class="tabbox"]/table/tbody/tr[@class="center"][position()<4]/td[position()<3]/span[@class="detail-company-name"]/text()'''
    ).extract()
    print('res0',res0)


    #
    # for each in res0:
    #     res0=each.xpath(
    #         # '//div[@class="table"][6]/div[@class="tabbox"]/table/tbody/tr[@class="center"]/td[position()<3]/text()'
    #         './td[position()<3]/text()'
    #
    #     ).extract()
    #     print('res00',res0)
    #     # res0[0:6])


    # res=Selector(text=html_text).xpath('//div[@class="table"][6]/div[@class="tabbox"]/table/tbody/tr[@class="center"]/td[1]/text()').extract()
    # print('res',res)
    # print('res',res[0:3])



    res_o= Selector(text=html_text).xpath(
        '//div[@class="table"][6]/div[@class="tabbox"]/table/tbody/tr[@class="center"]')

    print('res_o',res_o.xpath('/td[1]/text()').extract())







    '''
      '//div[@class="table"][1]/div[@class="tabbox"]/table//tbody[@id="searchResultTable"]//td[@style="border: none"]/text()').extract()
    '''
    res_base = Selector(text=html_text).xpath(
        '//div[@class="table"][1]/div[@class="tabbox"]/table//tbody[@id="searchResultTable"]//td[@style="border: none"]/text()').extract()

    print('res_base',res_base,)
    print('res_base list',res_base[0],res_base[1],res_base[5])



