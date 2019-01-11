# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest
from urllib import request
import  ssl
import os
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
from mihua.items import DmozItem,DetailItem
from scrapy.utils.project import get_project_settings
import json
from scrapy.exceptions import CloseSpider
from urllib.parse import urlparse,urlunparse,urljoin
from scrapy.selector import Selector




print(os.path.abspath('.'))



'''
第一步、
爬虫的第一次访问，一般用户登录时，第一次访问登录页面时，后台会自动写入一个Cookies到浏览器，所以我们的第一次主要是获取到响应Cookies
首先访问网站的登录页面，如果登录页面是一个独立的页面，我们的爬虫第一次应该从登录页面开始，如果登录页面不是独立的页面如 js 弹窗，那么我们的爬虫可以从首页开始
'''

class DoubanLoginSpider(scrapy.Spider):

    cookie = settings['MY_ORDER_COOKIE']
    headers = {
        'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',  # 保持链接状态
        'Referer': 'http://manage.sanjuhui.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',

    }  # 这是请求头，用来伪装成浏览器行为


    name = 'mihua_post_data'
    # allowed_domains = ['douban.com']
    start_urls = ["http://manage.sanjuhui.com/modules/manage/borrow/repay/urge/collection/list.htm"]


    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #     'mihua.pipelines.MihuaPipeline_post_data_spider': 300,
    #     }
    # }


    # UserAgent = {"User-Agent:":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2050.400 QQBrowser/9.5.10169.400"}
    def __init__(self):
        super(DoubanLoginSpider,self).__init__()
        self.detail_request_counts = 0
        self.all_pages=0
        self.total_data_counts=0

    def start_requests(self):
        return [scrapy.FormRequest(
            self.start_urls[0],
            cookies=self.cookie,
            headers=self.headers,
            # meta=self.meta
            formdata={'pageSize': '10', 'current': '1'},
            callback=self.parse)
        ]

    def parse(self, response):
        # 写到文件中,看是否下载成功
        print('response', response.body)
        # with open('/Users/ozintel/Downloads/Tsl_python_progect/local_ml/mihua/mihua/data/content.html', 'wb') as file:
        #     file.write(response.body)
        #     file.close()
        item = DmozItem()
        content = json.loads(response.body)
        print('content', content)
        data = content['data']
        item['data'] = data


        current_page = content['page']['current']
        item['current_page'] = current_page
        if  current_page==1:
            self.all_pages = content['page']['pages']
            self.total_data_counts = content['page']['total']


        item['pages'] = self.all_pages
        # item['total_data_counts']=self.total_data_counts


        #获取detail信息
        '''
        http://manage.sanjuhui.com/modules/manage/cl/cluser/detail.htm
        userId: 89884
        
        http://manage.sanjuhui.com/modules/manage/cl/cluser/detail.htm
        userId: 89829
        '''
        for each_borrowUserId in data:
            print('self.detail_request_counts={},each_borrowUserId '.format(self.detail_request_counts), each_borrowUserId)
            self.detail_request_counts=self.detail_request_counts+1
            yield scrapy.FormRequest(
                'http://manage.sanjuhui.com/modules/manage/cl/cluser/detail.htm',
                cookies=self.cookie,
                headers=self.headers,
                # meta=self.meta
                formdata={'userId': str(each_borrowUserId['borrowUserId'])},#borrowUserId
                callback=self.get_detail)



            '''获取report 信息'''
            '''
                    1.Request URL: http://manage.sanjuhui.com/modules/manage/tongdun/report.htm?pageSize=5&current=1&userId=89884
            Request Method: GET

                    2.Request URL: https://tenant.51datakey.com/carrier/mxreport_data/reportBasic?data=aX92rOy5T06Q%2FSuP0eVrRE1IibeVkuuE3E5AaZD8Styw83qrUN0BqUo2QYYp1cpbfh2HNnVVdfEmtTqs%2F44PNZWGMERQnPTFCrW873BDR4T3hmK61GFdbQfYPjCiFZeXSURqsDNiXEA10OV9hT5C%2BfEtDIj%2FZeFeWRflHihrRZ4B31X%2FIqJawW2MCHmGoH2M&contact=&mobile=13149357244&taskId=d8f40720-0e4e-11e9-9f12-00163e0f4b67&inputliveaddress=
            Request Method: GET
                    '''

            yield Request(
                url='http://manage.sanjuhui.com/modules/manage/tongdun/report.htm?pageSize=5&current={}&userId={}'.format(current_page,str(each_borrowUserId['borrowUserId'])),
                cookies=self.cookie,
                headers=self.headers,
                callback=self.get_report)



            # yield [FormRequest.from_response(response,
            #                               url="http://manage.sanjuhui.com/modules/manage/cl/cluser/detail.htm",  # 真实post地址
            #                               meta={"cookiejar":response.meta["cookiejar"]},
            #                               headers = self.headers,
            #                               formdata={'userId': each_borrowUserId['borrowUserId']},#borrowUserId,
            #                               callback=self.get_detail,
            #                               )]





        print('current_page<all_pages', current_page, self.all_pages)
        yield item
        if current_page <self.all_pages:
            yield scrapy.FormRequest(
                self.start_urls[0],
                cookies=self.cookie,
                headers=self.headers,
                # meta=self.meta
                formdata={'pageSize': '10', 'current': str(current_page + 1)},
                callback=self.parse)
        else:
            print('my_order finished')
            # raise CloseSpider#手动终止爬虫






            #这个是get的请求，把链接写错了所以出问题
            # Request(
            # url='http://manage.sanjuhui.com/modules/manage/borrow/repay/urge/collection/list.htm?pageSize=10&current={}&searchParams=%7B%22state%22%3A%2211%22%7D'.format(
            #     current_page + 1), callback=self.parse)







    def get_detail(self,response):
        print('response.body', response.body)
        # with open('/Users/ozintel/Downloads/Tsl_python_progect/local_ml/mihua/mihua/data/detail.html', 'wb') as file:
        #     file.write(response.body)
        #     file.close()

        item = DetailItem()
        content = json.loads(response.body)
        all_contach_info = content['data']['userContactInfo']
        # for each in all_contach_info:
        #     print('each', each['name'], each['phone'], each['relation'])

        item['import_name']=all_contach_info[0]['name']
        item['import_contact']=all_contach_info[0]['phone']
        item['import_relation']=all_contach_info[0]['relation']
        item['other_name']=all_contach_info[1]['name']
        item['other_contact']=all_contach_info[1]['phone']
        item['other_relation']=all_contach_info[1]['relation']
        item['detail_user_id']=content['data']['userbase']['userId']
        item['detail_user_name'] = content['data']['userbase']['realName']
        item['total_data_counts'] = self.total_data_counts

        yield item

    def get_report(self,response):
        content = json.loads(response.body)
        print('get_report content',content)
        url=content['url']
        url =url.replace('mxreport_data','mxreport_data/reportBasic')



        yield Request(
            url=url,
            cookies = self.cookie,
            headers = self.headers,
            callback=self.get_report_data)


    def get_report_data(self,response):
        with open('/Users/ozintel/Downloads/Tsl_python_progect/local_ml/mihua/mihua/data/repoert_data.html', 'wb') as file:
            file.write(response.body)
            file.close()
        content = json.loads(response.body)
        print('get_report_data content',content)
        result_data=content['result']
        # 取第6张表格的内容,td中的第一个;取前三个电话话号码
        num_list = Selector(text=result_data).xpath(
            '//div[@class="table"][6]/div[@class="tabbox"]/table/tbody/tr[@class="center"]/td[1]/text()').extract()[0:3]
        print('num_list',num_list)






                # def start_requests(self):
    #     """第一次请求一下登录页面，设置开启cookie使其得到cookie，设置回调函数"""
    #     #表示开启cookie记录，首次请求时写在Request()里
    #
    #
    #
    #     return [Request(
    #         self.start_urls[0],
    #         headers=self.headers,
    #         callback=self.Login,
    #         meta={"cookiejar":1})]

    # def parse(self, response):
    #     print('开始登陆',response.body)
    #     with open(r'/Users/ozintel/Downloads/Tsl_python_progect/local_ml/mihua/mihua/data/post_data.html', 'wb') as f:
    #         f.write(response.body)
    #     # # 查看一下响应Cookie，也就是第一次访问注册页面时后台写入浏览器的Cookie
    #     # Cookie1 = response.headers.getlist('Set-Cookie')  # 查看一下响应Cookie，也就是第一次访问注册页面时后台写入浏览器的Cookie
    #     # print('响应Cookie1:',Cookie1)
    #
    #
    #     # captcha = response.xpath("//img[@id='captcha_image']/@src").extract()
    #     # print('captcha',captcha)
    #     # if len(captcha) > 0:
    #     #
    #     #         # '''此时有验证码'''
    #     #         # 人工输入验证码
    #     #     print("正在保存验证码图片")
    #     #
    #     #
    #     #     captchapicfile = "../data/captcha.png"
    #     #     # urlopen = urllib.URLopener()
    #     #     # 下载图片流
    #     #     ssl._create_default_https_context = ssl._create_unverified_context
    #     #
    #     #     with request.urlopen(captcha[0]) as fp:
    #     #         data = fp.read()
    #     #         # 清除并以二进制写入
    #     #         f = open(captchapicfile, 'wb')
    #     #         f.write(data)
    #     #         f.close()
    #     #
    #     #     # request.urlretrieve(captcha[0],filename = captchapicfile)
    #     #     print("打开图片文件，查看验证码，输入单词......")
    #     #     captcha_value = input()
    #     #
    #     #     data = {
    #     #         "form_email":"1330065671@qq.com",
    #     #         "form_password":"LW199112262315.",
    #     #         "captcha-solution":captcha_value,
    #     #         "redir": "https://www.douban.com/note/645728300/",  #设置需要转向的网址，由于我们需要爬取个人中心页，所以转向个人中心页
    #     #
    #     #     }
    #     # else:
    #
    #          # '''此时无验证码'''
    #     # data = {
    #     #         "username": "zdcs01",
    #     #         "password": "wRMHhc9ocGjs7p",
    #     #         # "redir": "https://www.douban.com/note/645728300/",  #设置需要转向的网址，由于我们需要爬取个人中心页，所以转向个人中心页
    #     #
    #     #     }
    #     #
    #     # print("正在登陆中……")
    #     # #meta={'cookiejar':response.meta['cookiejar']}表示使用上一次response的cookie，写在FormRequest.from_response()里post授权
    #     # """第二次用表单post请求，携带Cookie、浏览器代理、用户登录信息，进行登录给Cookie授权"""
    #     # #通过分析表单得到，通过chrome的network看不出来
    #     # return [FormRequest.from_response(response,
    #     #                                   url="http://manage.sanjuhui.com/system/user/login.htm",  # 真实post地址
    #     #                                   meta={"cookiejar":response.meta["cookiejar"]},
    #     #                                   headers = self.headers,
    #     #                                   formdata = data,
    #     #                                   callback=self.crawlerdata,
    #     #                                   )]
    #
    # def crawlerdata(self,response):
    #     with open(r'../data/login_end.html','wb') as f:
    #         f.write(response.body)
    #
    #     print("完成登录.........")
    #     # title = response.xpath("/html/head/title/text()").extract()
    #     # content2 = response.xpath("//meta[@name='description']/@content").extract()
    #     # print(title[0])
    #     # print(content2[0])
    #     #
    #     # url='https://www.douban.com/people/36771726/statuses'
    #     # """登录后，请求需要登录才能查看的页面，如个人中心，携带授权后的Cookie请求"""
    #     # yield Request(url,
    #     #               headers=self.headers,
    #     #               meta={'cookiejar':True},#表示使用授权后的cookie访问需要登录查看的页面
    #     #               callback=self.parse_item)
    #
    #
    # # def parse_item(self, response):
    # #     # 请求Cookie
    # #     Cookie2 = response.request.headers.getlist('Cookie')
    # #     print('请求cookie2',Cookie2)
    # #     with open(r'/Users/ozintel/Tsl_exercise/znfw_crawer/douban_post_login/data/item.html','wb') as f:
    # #         f.write(response.body)
    # #     url='https://www.douban.com/note/645728300/'
    # #     yield Request(url,
    # #                   headers=self.headers,
    # #                   meta={'cookiejar': True},  # 表示使用授权后的cookie访问需要登录查看的页面
    # #                   callback=self.parse_item2)
    # #
    # # def parse_item2(self, response):
    # #     # 请求Cookie
    # #     Cookie3 = response.request.headers.getlist('Cookie')
    # #     print('查看需要登录才可以访问的页面携带Cookies：', Cookie3)
    # #     with open(r'/Users/ozintel/Tsl_exercise/znfw_crawer/douban_post_login/data/item2.html','wb') as f:
    # #         f.write(response.body)

