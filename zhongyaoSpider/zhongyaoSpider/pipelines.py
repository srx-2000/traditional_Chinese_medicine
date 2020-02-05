# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import os
class ZhongyaospiderPipeline(object):
    def process_item(self, item, spider):
        # 获取当前工作目录
        base_dir = os.getcwd()
        fiename = base_dir + '/zhongyao.txt'
        # 从内存以追加的方式打开文件，并写入对应的数据
        # for i in item['zhongyao']:
        #     line.join(item['zhongyao'])
        #print(item['zhongyao_name'])
        with open(fiename, 'a',encoding='utf-8') as f:
            f.writelines(item['zhongyao_name'])
            f.write('\n')
            f.writelines(item['zhongyao'])
            f.write('\r\n')
        logging.debug("写入一个")
    def close_spider(self,spider):
        self.file.close()