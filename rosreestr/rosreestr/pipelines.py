# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from json import  dumps
from codecs import getwriter
from sys import stdout
import datetime

class RosreestrPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.reestr = set()
    def process_item(self, item, spider):
        sout = getwriter("utf8")(stdout)
        if not item['address'] in self.reestr:
            self.reestr.add(item['address'])
            sout.write(dumps(dict(item), ensure_ascii=False) + "\n")
        return item

