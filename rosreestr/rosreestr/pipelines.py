# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import datetime

class RosreestrPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):

    def __init__(self):
        now = datetime.datetime.now()
        now = now.strftime("%d%m%Y%H%M")
        self.file = codecs.open('rosreestr_'+now+'.json', 'w', "utf-8")

    def process_item(self, item, spider):
        item['address'] = item['address']
        line = json.dumps(dict(item), ensure_ascii=False) + ","
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()