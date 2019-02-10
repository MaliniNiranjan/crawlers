# -*- coding: utf-8 -*-
import scrapy
import MySQLdb


class MutualfundholdingsSpider(scrapy.Spider):
		name = "mutualfundholdings"

		def __init__(self, *args, **kwargs):
			super(MutualfundholdingsSpider, self).__init__(*args, **kwargs)
			self.conn=MySQLdb.connect(db='MINE',host='localhost',user='root', passwd ='malini.123', charset='utf8',use_unicode=True)
			self.cursor = self.conn.cursor()

		def start_requests(self):
			query = "select queue from mutalfunds"
			self.cursor.execute(query)
			records = self.cursor.fetchall()
			records = [ record[0] for record in records]
			for record in records:
				yield scrapy.Request(record,callback=self.parse)

		def parse(self, response):
			holdings= response.xpath('//div//table[@class="tblporhd"]//tr')
			holdings = holdings[1:]
			sk = response.url.split("/")[-1]
			for holding in holdings:
				equity, sector, qty, value, percentage	= holding.xpath('.//text()').extract()
				yield {'equity' : equity, 'sector' : sector,'qty' : qty , 'value': value, 'percentage' : percentage, 'sk' : sk}	
