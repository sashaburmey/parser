# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from json import  dumps
import json
from codecs import getwriter
from sys import stdout
import logging
import  jsonschema

class SocietPipeline(object):

    def __init__(self):
        self.sout = getwriter("utf8")(stdout)
        logger = logging.getLogger()
        self.soceite = set()
        try:
            self.schema = open("locations.schema.json").read()
        except:
            logger.error('Cannot open schema')

    def process_item(self, item, spider):
        logger = logging.getLogger()
        try:
            jsonschema.validate(dict(item), json.loads(self.schema))
            if not item['link'] in self.soceite:
                self.soceite.add(item['link'])
                self.sout.write(dumps(dict(item), ensure_ascii=False) + "\n")
        except jsonschema.ValidationError as e:
            logger.error(e.message + ' ' + item['link'] )
        except jsonschema.SchemaError as e:
            logger.error(e)
        return item
