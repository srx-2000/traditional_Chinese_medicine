# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
#这个类一定要激活 配置文件中激活
class MedicinePipeline(object):

    def __init__(self):
        #初始化 文件对象
        self.f = open(r'C:\Users\taomin\Desktop\medicinetwo.csv','a',encoding='utf-8',newline = '')
        self.csvWriter = csv.writer(self.f)#初始化csv文件对象
        # 表头，列名
        self.header = [
            '名字',
            '拼音名',
            '别名',
            '来源',
            '性味',
            '功能主治',
            '用法用量',
            '摘录',
        ]
        self.csvWriter.writerow(self.header)

    #这个函数用来写入数据
    def process_item(self, item, spider):
        '''
        写入文件
        :param item: 就是爬虫items返回的数据
        :param spider: 就是这个类SpidersSpider实例化的结果
        :return: item必须写，否则下一个（如果有）接受不到数据  就保存不了了
       '''
        # 写入文件一定要是列表格式
        data = [
            item.get('name', ''),
            item.get('phonetic', ''),
            item.get('other_name',''),#如果取不出来就为空
            item.get('origine', ''),
            item.get('taste', ''),
            item.get('function', ''),
            item.get('usage', ''),
            item.get('extract', ''),

        ]
        self.csvWriter.writerow(data)

        return item

    def close_spider(self,spider):
        #关闭文件
        self.f.close()