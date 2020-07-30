# -*- coding: utf-8 -*-
import scrapy #脚手架工具#项目下有多个爬虫
from ..items import MedicineItem

#医药卫生网

#创建爬虫类
class SpidersSpider(scrapy.Spider):
    name = 'medicinespider'#爬虫名字-->必须唯一
    start_urls = [f'http://py.yywsb.com/zyzy_list2.asp?page={page}&id=554' for page in range(1,83)]#爬虫第一次开始采集的网址   【f'https://www.zhzyw.com/zycs/zycd/a.html' for i in range()】 多页是
    print(start_urls)

   #反爬
    #custom_settings = None

    #解析响应数据，处理返回的网页数据，网址等
    #response 这个形式参数就是网页源码
    def parse(self, response):
        #提取数据
        # pages = response.xpath("//div[@class='Areathree4']/font[@color='red']/text()").extract()
        # if pages:
        #     if pages[0]<pages[1]:
        #         next_page_url = "http://py.yywsb.com/zyzy_list2.asp?page={}&id=554".format(int(pages[0])+1)
        #         print('下一页的链接',next_page_url)
        #         print(1)
        #         #发出请求  Request callback 是回调函数 就是将请求的得到的响应交给自己处理
        #         yield scrapy.Request(next_page_url, callback=self.parse)
        details = response.xpath("//div[@class='Areasub3']/ul/li/a/@href").extract()
        for i in details:
            details_url = "http://py.yywsb.com/" + i
            yield scrapy.Request(details_url, callback=self.details_parse)

    def details_parse(self, response):
        Item = MedicineItem()
        Item['name'] = response.xpath("//div[@class='Areathree1']/text()")[0].extract()
        medicine_context_html = response.xpath("//div[@class='Areathree3']/a[1]/p")
        if len(medicine_context_html)==0:
            medicine_context_html = response.xpath("//div[@class='Areathree3']/p")
        for context_html in medicine_context_html:
            context = context_html.xpath("string(.)")
            if context.re("【拼音.*"):
                phonetics= context.extract()[0]
                if len(phonetics)>0:
                    Item['phonetic'] = phonetics[5:]
            if context.re("【别名.*"):
                other_names= context.extract()[0]
                if len(other_names)>0:
                    Item['other_name'] = other_names[4:]
            if context.re("【来源.*"):
                origines= context.extract()[0]
                if len(origines)>0:
                    Item['origine'] = origines[4:]
            if context.re("【性味.*"):
                tastes= context.extract()[0]
                if len(tastes)>0:
                    Item['taste'] = tastes[4:]
            if context.re("【功能.*"):
                functions= context.extract()[0]
                if len(functions)>0:
                    Item['function'] = functions[6:]
            if context.re("【用法.*"):
                usages= context.extract()[0]
                if len(usages)>0:
                    Item['usage'] = usages[6:]
            if context.re("【摘录.*"):
                extracts= context.extract()[0]
                if len(extracts)>0:
                    Item['extract'] = extracts[4:]

        yield Item  # 生成器返回
        # 这里可以保存，但复杂性高
        # with open() as fp:
        #     fp.write()write








# #医药卫生网
#
# #创建爬虫类
# class SpidersSpider(scrapy.Spider):
#     name = 'medicine'#爬虫名字-->必须唯一
#     start_urls = [f'http://py.yywsb.com/zyzy_list2.asp?page={page}&id=554' for page in range(1,139)]#爬虫第一次开始采集的网址   【f'https://www.zhzyw.com/zycs/zycd/a.html' for i in range()】 多页是
#     print(start_urls)
#
#    #反爬
#     #custom_settings = None
#
#     #解析响应数据，处理返回的网页数据，网址等
#     #response 这个形式参数就是网页源码
#     def parse(self, response):
#         #提取数据
#         # pages = response.xpath("//div[@class='Areathree4']/font[@color='red']/text()").extract()
#         # if pages:
#         #     if pages[0]<pages[1]:
#         #         next_page_url = "http://py.yywsb.com/zyzy_list2.asp?page={}&id=554".format(int(pages[0])+1)
#         #         print('下一页的链接',next_page_url)
#         #         print(1)
#         #         #发出请求  Request callback 是回调函数 就是将请求的得到的响应交给自己处理
#         #         yield scrapy.Request(next_page_url, callback=self.parse)
#         details = response.xpath("//div[@class='Areasub3']/ul/li/a/@href").extract()
#         for i in details:
#             details_url = "http://py.yywsb.com/" + i
#             yield scrapy.Request(details_url, callback=self.details_parse)
#
#     def details_parse(self, response):
#         Item = SpidersSpiderItem()
#         Item['name'] = response.xpath("//div[@class='Areathree1']/text()")[0].extract()
#         medicine_context_html = response.xpath("//div[@class='Areathree3']/a[1]/p")
#         if len(medicine_context_html)==0:
#             medicine_context_html = response.xpath("//div[@class='Areathree3']/p")
#         for context_html in medicine_context_html:
#             context = context_html.xpath("string(.)")
#             if context.re("【拼音.*"):
#                 phonetics= context.extract()[0]
#                 if len(phonetics)>0:
#                     Item['phonetic'] = phonetics[5:]
#             if context.re("【别名.*"):
#                 other_names= context.extract()[0]
#                 if len(other_names)>0:
#                     Item['other_name'] = other_names[4:]
#             if context.re("【来源.*"):
#                 origines= context.extract()[0]
#                 if len(origines)>0:
#                     Item['origine'] = origines[4:]
#             if context.re("【性味.*"):
#                 tastes= context.extract()[0]
#                 if len(tastes)>0:
#                     Item['taste'] = tastes[4:]
#             if context.re("【功能.*"):
#                 functions= context.extract()[0]
#                 if len(functions)>0:
#                     Item['function'] = functions[6:]
#             if context.re("【用法.*"):
#                 usages= context.extract()[0]
#                 if len(usages)>0:
#                     Item['usage'] = usages[6:]
#             if context.re("【摘录.*"):
#                 extracts= context.extract()[0]
#                 if len(extracts)>0:
#                     Item['extract'] = extracts[4:]
#
#         yield Item  # 生成器返回
#         # 这里可以保存，但复杂性高
#         # with open() as fp:
#         #     fp.write()write





#中药材，中药世家网

# #创建爬虫类
# class SpidersSpider(scrapy.Spider):
#     name = 'medicine'#爬虫名字-->必须唯一
#     #allowed_domains = ['http://www.zysj.com','http://www.zysj.com.cn/zhongyaocai/index__1.html>']#爬虫域名爬虫只在这个网站下采集，可以注释
#     start_urls = [f'http://www.zysj.com.cn/zhongyaocai/index__{page}.html' for page in range(1,24)]#爬虫第一次开始采集的网址   【f'https://www.zhzyw.com/zycs/zycd/a.html' for i in range()】 多页是
#     print(start_urls)
#         # 反爬
#         # custom_settings = None
#
#         # 解析响应数据，处理返回的网页数据，网址等
#         # response 这个形式参数就是网页源码
#     def parse(self, response):
#         # 提取数据
#         details = response.xpath("//div[@id='content']/ul/li/a/@href").extract()
#         for i in details:
#             details_url = "http://www.zysj.com.cn" + i
#             print(details_url)
#             yield scrapy.Request(details_url, callback=self.details_parse)
#
#     def details_parse(self, response):
#
#         name = response.xpath("//div[@id='content']/h1/text()")[0].extract()
#         pingyint= response.xpath("//div[@id='content']/p[@class='drug py']/text()").extract()  # 为获取真实的原文数据，需用extract提出出来,数据在对象里面可以('./a/text()').get()
#         pingyin = []
#         if len(pingyint)>1:
#             pingyin = pingyint[1]
#         elif len(pingyint)==1:
#             pingyin = pingyint[0]
#         biemingt = response.xpath("//div[@id='content']/p[@class='drug bm']/text()").extract()
#         bieming = []
#         if len(biemingt) > 1:
#             bieming = biemingt[1]
#         elif len(biemingt) == 1:
#             bieming = biemingt[0]
#         laiyuan = response.xpath("//div[@id='content']/p[@class='drug ly']/text()").extract()
#         laiyuat = response.xpath("//div[@id='content']/p[@class='drug ly']")
#         laiyuant = laiyuat.xpath('string(.)').extract()
#         laiyuan = []
#         if len(laiyuant) > 1:
#             laiyuan = laiyuant[1]
#         elif len(laiyuant) == 1:
#             laiyuan = laiyuant[0]
#         xingweit = response.xpath("//div[@id='content']/p[@class='drug xw']/text()").extract()
#         xingwei = []
#         if len(xingweit) > 1:
#             xingwei = xingweit[1]
#         elif len(xingweit) == 1:
#             xingwei = xingweit[0]
#         gongnengt = response.xpath("//div[@id='content']/p[@class='drug gnzz']/text()").extract()
#         gongneng = []
#         if len(gongnengt) > 1:
#             gongneng = gongnengt[1]
#         elif len(gongnengt) == 1:
#             gongneng = gongnengt[0]
#         yongfat = response.xpath("//div[@id='content']/p[@class='drug yfyl']/text()").extract()
#         yongfa = []
#         if len(yongfat) > 1:
#             yongfa = yongfat[1]
#         elif len(yongfat) == 1:
#             yongfa = yongfat[0]
#         zhailuet = response.xpath("//div[@id='content']/p[@class='drug zl']/text()").extract()
#         zhailue = []
#         if len(zhailuet) > 1:
#             zhailue = zhailuet[1]
#         elif len(zhailuet) == 1:
#             zhailue = zhailuet[0]
#
#         # 返回数据  用来保存数据
#         # 返回的数据 必须是类似字典格式
#
#         items = {
#             'name': name,
#             'pingyin': pingyin,
#             'bieming': bieming,
#             'laiyuan': laiyuan,
#             'xingwei': xingwei,
#             'gongneng': gongneng,
#             'yongfa': yongfa,
#             'zhailue': zhailue,
#         }
#         yield items  # 生成器返回
#         # 这里可以保存，但复杂性高
#         # with open() as fp:
#         #     fp.write()write




#中医中药网

# class SpidersSpider(scrapy.Spider):
#     name = 'medicine'#爬虫名字-->必须唯一
#     allowed_domains = ['zhzyw.com','zhzyw.com/zycs/zycd/a.html']#爬虫域名爬虫只在这个网站下采集，可以注释
#     start_urls = [f'https://www.zhzyw.com/zycs/zycd/{chr(page)}.html' for page in range(97,123)]#爬虫第一次开始采集的网址   【f'https://www.zhzyw.com/zycs/zycd/a.html' for i in range()】 多页是
#     print(start_urls)
#
#    #反爬
#     #custom_settings = None
#
#     #解析响应数据，处理返回的网页数据，网址等
#     #response 这个形式参数就是网页源码
#     def parse(self, response):
#         #提取数据
#         next_page = response.xpath("//a[@title='下一页']/@href").extract()
#         if next_page:
#             for i in next_page:
#                 next_url = "https://www.zhzyw.com" + i
#                 print('下一页的链接',next_url)
#                 #发出请求  Request callback 是回调函数 就是将请求的得到的响应交给自己处理
#                 yield scrapy.Request(next_url, callback=self.parse)
#         else:
#             next_Letter = response.xpath("//div[@id='piny']/a[position()>=2]/@href").extract()
#             for i in next_Letter:
#                 next_Letter_url = "https://www.zhzyw.com/zycs/zycd/" + i
#                 yield scrapy.Request(next_Letter_url, callback=self.parse)
#         details = response.xpath("//div[@class='ullist01']/ul/li/a/@href").extract()
#         for i in details:
#             details_url = "https://www.zhzyw.com" + i
#             yield scrapy.Request(details_url, callback=self.details_parse)
#
#     def details_parse(self, response):
#         # dic={}
#         content_next_page = response.xpath("//div[@class='pagecontent']/a[@title='下一页']/@href").extract()
#         if content_next_page:
#             for i in content_next_page:
#                 content_next_url = response.urljoin(i)
#                 yield scrapy.Request(content_next_url, callback=self.details_parse)
#         logging.debug("使用")
#         # from pachong.zhongyaoSpider.zhongyaoSpider.items import ZhongyaospiderItem
#         medicine_name = response.xpath("//div[@id='left']/h1/text()").extract()
#         medicine = response.xpath("//div[@class='webnr']/p/text()").extract()#为获取真实的原文数据，需用extract提出出来,数据在对象里面可以('./a/text()').get()
#                                                                                      # get获取一个元素，getall()获取多个或.extract_first()
#         print(1,medicine_name,2,medicine)
#
#         #返回数据  用来保存数据
#         #返回的数据 必须是类似字典格式
#
#         items = {
#             'medicine_name':medicine_name,
#             'medicine':medicine,
#         }
#         yield items#生成器返回
#             #这里可以保存，但复杂性高
#             # with open() as fp:
#             #     fp.write()