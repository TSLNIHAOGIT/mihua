import json
from scrapy.selector import Selector
'''content'''

path='/Users/ozintel/Downloads/Tsl_python_progect/local_ml/mihua/mihua/data/repoert_data.html'
import pandas as pd

body = '<body><span>good</span></body>'
res_body=Selector(text=body).xpath('//span/text()').extract()
print('res_body',res_body)


with open(path, 'r') as f:
    data = json.load(f)
    print(data)
    html_text=data['result']
    #取第6张表格的内容,td中的第一个
    res=Selector(text=html_text).xpath('//div[@class="table"][6]/div[@class="tabbox"]/table/tbody/tr[@class="center"]/td[1]/text()').extract()
    print('res',res)
    print('res',res[0:3])
