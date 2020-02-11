# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import csv
class ZhongyiyaospiderPipeline(object):
    def __init__(self):
        base_dir = os.getcwd()
        fiename = base_dir + '/zhongyao2.csv'
        print("*" * 80)
        self.file = open(fiename, 'a+', encoding='utf_8_sig', newline='')
        self.writer = csv.writer(self.file, dialect="excel")

    def process_item(self, item, spider):
        print("正在写入.............")
        if item["name"]:
            self.writer.writerow([item["name"], item["piny"],item['other_name'],item['laiyuan'],item['xingwei'],item['gongneng'],item['yongfa'],item['zhailu']])
            return item

