# coding: utf8
import scrapy
import re
from societ.items import SocietItem
import logging
class SocieteteSpider(scrapy.Spider):
    handle_httpstatus_list = [302]
    name = "societe"
    def read_dict(self):
        logger = logging.getLogger()
        try:
            fp = open('francais.txt','r')
            french_dict = fp.read().split('\n')
            fp.close()
            return french_dict
        except IOError:
            logger.error('Cannot open french dict!')


    def start_requests(self):
        words = self.read_dict()
        for word in words:
            url = 'http://www.societe.com/cgi-bin/liste?nom='+word.upper()
            yield scrapy.Request(url=url, callback=self.parse_link)


    def parse_link(self, response):
        urls = response.xpath(".//a[@class='linkresult']/@href").extract()
        for url in urls:
            yield scrapy.Request(url=response.urljoin(url), callback=self.parse_item)

    def parse_item(self, response):
        stat = response.xpath(".//table[@id='rensjur']/tr[position()=1]/td[position()=1]/text()").extract_first()
        if stat=='Statut':
            societe_item = SocietItem()
            societe_item['name'] = response.xpath(".//table[@id='rensjur']/tr[position()=2]/td[position()=2]/text()").extract_first(default=' ')
            societe_item['address'] = response.xpath(".//table[@id='rensjur']/tr[position()=3]/td[position()=2]/a/text()").extract_first(default=' ').strip()
            societe_item['link'] = response.url
            societe_item['category'] = response.xpath(".//table[@id='rensjur']/tr[position()=7]/td[position()=2]/text()").extract_first(default=' ')
        elif stat=='Jugement':
            societe_item = SocietItem()
            societe_item['name'] = response.xpath(".//table[@id='rensjur']/tr[position()=2]/td[position()=2]/text()").extract_first(default=' ')
            societe_item['address'] = response.xpath(".//table[@id='rensjur']/tr[position()=3]/td[position()=2]/a/text()").extract_first(default=' ').strip()
            societe_item['link'] = response.url
            if societe_item['address'] == ' ':
                societe_item['category'] = response.xpath(".//table[@id='rensjur']/tr[position()=7]/td[position()=2]/text()").extract_first(default=' ')
            else:
                societe_item['category'] = response.xpath(".//table[@id='rensjur']/tr[position()=8]/td[position()=2]/text()").extract_first(default=' ')
        else:
            societe_item = SocietItem()
            societe_item['name'] = response.xpath(".//table[@id='rensjur']/tr[position()=1]/td[position()=2]/text()").extract_first(default=' ')
            societe_item['address'] = response.xpath(".//table[@id='rensjur']/tr[position()=2]/td[position()=2]/a/text()").extract_first(default=' ').strip()
            societe_item['link'] = response.url
            if societe_item['address']==' ':
                societe_item['category'] = response.xpath(".//table[@id='rensjur']/tr[position()=6]/td[position()=2]/text()").extract_first(default=' ')
            else:
                societe_item['category'] = response.xpath(".//table[@id='rensjur']/tr[position()=7]/td[position()=2]/text()").extract_first(default=' ')
        yield societe_item


