# coding: utf8
import scrapy
import json
from accorhotels.items import AccorhotelsItem
class AsosSpider(scrapy.Spider):
    handle_httpstatus_list = [300]
    name = "accor"
    count = 0
    def start_requests(self):
        url = 'https://secure.accorhotels.com/rest/v2.0/accorhotels.com/hotels?geoCode=PFR&geoType=PA'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        json_accord = json.loads(response.body)

        for item in json_accord['zone']['child']:
            self.count = self.count + int(item['brandHotelNb'])
            url = 'https://secure.accorhotels.com/rest'+item['href']
            yield scrapy.Request(url=url, callback=self.parse1)

    def parse1(self, response):
        json_accord = json.loads(response.body)
        if json_accord['zone']['child']:
            for item in json_accord['zone']['child']:
                url = 'https://secure.accorhotels.com/rest' + item['href']
                yield scrapy.Request(url=url, callback=self.parse1)
        else:
            for item in json_accord['hotel']:
                accord_item = AccorhotelsItem()
                accord_item['name'] = item['name']
                accord_item['address'] = item['address']['country']+', '+item['address']['town']+', '+item['address']['street']
                accord_item['lat'] = item['address']['geoLoc']['latitude']
                accord_item['lon'] = item['address']['geoLoc']['longitude']
                if item['appartHotel']== True:
                    accord_item['category'] = 'appartment'
                else:
                    accord_item['category'] = 'hotel'
                url = 'http://www.accorhotels.com/fr/hotel-'+str(item['code'])+'-'+item['name'].replace(' ','-')+'/index.shtml'
                accord_item['url'] = item['bookUrl']
                atrr = []
                for k in item['amenities']:
                    atrr.append(k['label'])
                accord_item['attributes']= ', '.join(atrr)
                yield scrapy.Request(url=url, callback=self.parse2, meta={'accord_item': accord_item})


    def parse2(self, response):
        accord_item = response.meta['accord_item']
        accord_item['link'] = response.url
        accord_item['phone'] = response.xpath(".//meta[@itemprop='telephone']/@content").extract_first()
        print self.count
        yield accord_item
