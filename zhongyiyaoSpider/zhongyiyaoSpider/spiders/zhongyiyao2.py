# -*- coding: utf-8 -*-
import scrapy


class Zhongyiyao3Spider(scrapy.Spider):
    name = 'zhongyiyao2'
    allowed_domains = ['zxzycd.com']
    start_urls = [f'https://zxzycd.com/中药/{chr(page)}'for page in range(97,123)]

    def parse(self, response):
        for i in self.start_urls:
            if i == ("https://zxzycd.com/中药/a"):
                zhongyao_list = response.xpath("//div[@class='level2']/p/a/@href").extract()
            else:
                zhongyao_list=response.xpath("//div[@class='level1']/p/a/@href").extract()
                zhongyao_list_null=response.xpath("//div[@class='level1']/p/a/@rel").extract()
        if zhongyao_list_null:
            pass
        else:
            for i in zhongyao_list:
                zhongyao_content=response.urljoin(i)
                yield scrapy.Request(zhongyao_content,callback=self.detail_parse)
    def detail_parse(self,response):
        name = []
        piny = []
        other_name = []
        laiyuan = []
        xingwei = []
        yongfa = []
        zhailu = []
        gongneng=[]
        namet=response.xpath("//h2[@class='sectionedit2']/text()")
        if namet.re("^药典$"):
            name=response.xpath("//h3[@class='sectionedit3'or @class='sectionedit5']/text()")[0].extract()
            content=response.xpath("//div[@class='level3']/p/text()")
        else:
            name = response.xpath("//h2/text()")[0].extract()
            content = response.xpath("//div[@class='level2']/p/text()")
        if content:
            for i in content:
                if i.re("【来源.*"):
                    laiyuan=i.extract().strip()
                if i.re("【用法.*"):
                    yongfa=i.extract().strip()
                if i.re("【功能.*"):
                    gongneng=i.extract().strip()
                if i.re("【拼音.*"):
                    piny=i.extract().strip()
                if i.re("【别名.*"):
                    other_name=i.extract().strip()
                if i.re("【性味.*"):
                    xingwei=i.extract().strip()
                if i.re("【摘录.*"):
                    zhailu=i.extract().strip()
        item = {
                    "name": name,
                    "gongneng": gongneng,
                    'other_name': other_name,
                    "yongfa": yongfa,
                    "xingwei": xingwei,
                    "zhailu": zhailu,
                    "laiyuan": laiyuan,
                    "piny": piny
                }
        yield item
        # print(item)