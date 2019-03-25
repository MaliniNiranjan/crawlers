# -*- coding: utf-8 -*-
import scrapy


class AgriSpider(scrapy.Spider):
    name = "agri"
    start_urls = (
        'http://122.15.179.102/tnmarket/home/price_det/',
    )

    def parse(self, response):
		crop = response.xpath('//table//tr')
		for i in crop:
			crop_name = ''.join(i.xpath('.//td[3]/text()').extract())
			crop_variety =''.join(i.xpath('.//td[4]/text()').extract())
			link = ''.join(i.xpath('.//td[10]/a/@href').extract())
			name = "Malini"
			if link:
				yield scrapy.Request(link,callback=self.parse_page1 , meta= {'crop_name' : crop_name , 'crop_variety' : crop_variety , 'name': name})
				#import pdb;pdb.set_trace()
    def parse_page1(self,response):
		crop_table= response.xpath('//table//tr')
		#import pdb;pdb.set_trace()
		for i in crop_table:

			comittee = i.xpath('.//td[2]/text()').extract()
			comittee = ''.join(comittee[1:])
			RM_name =''.join(i.xpath('.//td[3]/text()').extract())
			QTY =''.join(i.xpath('.//td[4]/text()').extract())
			max_price = ''.join(i.xpath('.//td[5]/text()').extract())
			min_price = ''.join(i.xpath('.//td[6]/text()').extract())
			modal_price = ''.join(i.xpath('.//td[7]/text()').extract())
			print comittee
			print RM_name
			print QTY
			print max_price
			print min_price
			print modal_price
			if RM_name:
				yield{'crop_name' : response.meta['crop_name'], 'crop_variety': response.meta['crop_variety'],'comittee' : comittee,'RM_name' : RM_name , 'QTY' : QTY, 'max_price': max_price, 'min_price' : min_price , 'modal_price': modal_price}
