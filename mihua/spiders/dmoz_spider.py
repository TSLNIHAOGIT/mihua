import scrapy
import  urllib
import re
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
import time
# class DmozSpider(scrapy.Spider):
#     name = "dmoz"
#     allowed_domains = ["dmoz.org",'lihun66.com']
#     start_urls = [


#         "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
#         "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/",
#         "http://www.lihun66.com/ask/browser.php?tid2=2&page=1"
#     ]
#
#     def parse(self, response):
#         filename = response.url.split("/")[-2]
#         with open(filename, 'wb') as f:
#             f.write(response.body)

from mihua.items import DmozItem

class DmozSpider(scrapy.Spider):

    name = "mihua_temp"
    # allowed_domains = ["dmoz.org",'lihun66.com']
    '''Scrapy为Spider的 start_urls 属性中的每个URL创建了 scrapy.Request 对象，并将 parse 方法作为回调函数(callback)赋值给了Request'''
    start_urls = [
        "http://www.lawtime.cn/ask/browse_s4_p380.html"
    ]
    '''Request对象经过调度，执行生成 scrapy.http.Response 对象并送回给spider parse() 方法'''
    '''parse() 是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数。 
    该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象'''
    # def parse(self, response):
    #     print('***********response:',type(response),response.body)
    #     for sel in response.xpath('//ul/li'):
    #         item = DmozItem() #Item 对象是自定义的python字典。 您可以使用标准的字典语法来获取到其每个字段的值。(字段即是我们之前用Field赋值的属性
    #         item['title'] = sel.xpath('a/text()').extract()
    #         item['link'] = sel.xpath('a/@href').extract()
    #         item['desc'] = sel.xpath('text()').extract()
    #         yield item      #yield是一个关键词，类似return, 不同之处在于，yield返回的是一个生成器,Spider将会将爬取到的数据以 Item 对象返回
    def __init__(self):
        self.page=380
        self.state_count=0
    def parse(self, response):
       response_status=response.status
       print('状态码为：',response_status)
       response_url = response.url
       print('response_url:', response_url)
       if response_status==403:
           self.state_count=self.state_count+1

           # yield scrapy.FormRequest(
           #     url=url,
           #     formdata={"email": "xxx", "password": "xxxxx"},
           #     callback=self.parse_page
           # )

           with open(r'/Users/ozintel/Tsl_exercise/znfw_crawer/lihun/data/law.html','wb') as f:
               f.write(response.body)
           very_code = input('第%s次遇到验证码，请处理验证码:\n' % (self.state_count))
           print('已经输入验证码，继续抓取：')
           # time.sleep(5)


       # uri_list=response.xpath('//div[@class="list-block h100p o-h"]//dd//a/@href').extract()
       uri_list = response.xpath('//div[@class="list-main-l fl"]/a/@href').extract()#加入h4出错
       count_link=len(uri_list)
       print('页面链接数为：',count_link)


       if count_link==0 and response_status!=403:
           print('哈哈哈哈哈')
           raise CloseSpider()
       if count_link!=0 or response_status==403:
           for uri in uri_list:
                uri_1 =  uri
                print(uri_1)
                yield response.follow(url=uri_1, callback=self.parse_item_1)

            # if self.page<10:
            #     yield response.follow(url=uri_1, callback=self.parse_item_1)
            # elif self.page<163:
            #     yield response.follow(url=uri_1, callback=self.parse_item_2)
            # else:
            #     yield response.follow(url=uri_1, callback=self.parse_item_3)
       # uri_2 = response_url.replace('&page=%s' % page, '')
       self.page = self.page + 1
       # http: // www.lawtime.cn / ask / browse_s4_p13.html
       uri_2="http://www.lawtime.cn/ask/browse_s4_p%s.html" %(self.page)
       # "http://www.lawtime.cn/ask/browse_s4_p1.html"

       # item = DmozItem()  # 在item.py中定义好的，该字典将会被返回给pipeline调用**********
       # item['type'] = '%s' %page   # ***********
       # yield item


       yield scrapy.Request(url=uri_2, callback=self.parse)
    def parse_item_1(self, response):
        # with open(r'/Users/ozintel/Tsl_exercise/znfw_crawer/tutorial2/data/law.html','wb') as f:
        #     body=response.body
        #     print(body)
        #     f.write(body)
        item=DmozItem()#在item.py中定义好的，该字典将会被返回给pipeline调用


        title = ''.join(response.xpath('//div[@class="consult-question-contain"]//h1[@class="consult-question-title"]/text()').extract())
        item['title'] = re.sub('\s', '', title)

        item['text'] =''.join(response.xpath('//div[@class="consult-question-contain"]//p[@class="consult-question-detail"]/text()').extract())

        answer=''.join(response.xpath('//div[@class="consult-answer-detail-text"]/text()').extract())
        item['answer']=re.sub('\u3000\u3000|\r\n','',answer)

        # item['web_category'] = ''.join(
        #     response.xpath('//div[@class="lvshijieda-body"]//p//span[last()]/a/text()').extract())
        # print('item',item)
        yield item



    def parse_item2(self,response):
        l = ItemLoader(item=DmozItem(), response=response)
        l.add_xpath('type','//div[@class="location ask_main_location"]/span[@class="fl"]/a[last()]/text()')
        l.add_xpath('type','//div[@class="question"]/h2/text()')
        l.add_xpath('answer','//div[@class="anwser"]/h2/text()')
        l.add_value('answer','牛逼')
        yield l.load_item()





'''
parse() 是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数。 
该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象

Scrapy为Spider的 start_urls 属性中的每个URL创建了 scrapy.Request 对象，并将 parse 方法作为回调函数(callback)赋值给了Request。
Request对象经过调度，执行生成 scrapy.http.Response 对象并送回给spider parse() 方法。


'''