# -*- coding: utf-8 -*-
import scrapy

import re
class Zhongyiyao2Spider(scrapy.Spider):
    name = 'zhongyiyao1'
    allowed_domains = ['zd9999.com']
    start_urls = [f'http://www.zd9999.com/mf/htm0/{page}.htm' for page in range(1,8021)]

    def parse(self, response):
        name=[]
        piny = []
        other_name = []
        laiyuan = []
        xingwei = []
        yongfa = []
        zhailu = []
        gongneng=[]
        name=response.xpath("//font/b/text()")[0].extract()
        content=response.xpath("//td[br]/text()")
        if content:
            for i in content:
                if i.re("【来源.*"):
                    laiyuan=i.extract().strip()
                if i.re("【用法.*"):
                    yongfa=i.extract().strip()
                if i.re("【主治.*"):
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
