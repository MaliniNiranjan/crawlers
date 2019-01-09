# -*- coding: utf-8 -*-
import scrapy


class MutualfundsSpider(scrapy.Spider):
    name = "mutualfunds"
    start_urls = (
        'https://www.moneycontrol.com/mutual-funds/nav/axis-long-term-equity-fund-direct-plan/MAA192',
    )

    def parse(self, response):
	fund = ''.join(response.xpath('//h1[@class="pcstname"]//text()').extract()).strip()
	plan, option, typ, amfi_code = response.xpath('.//div/div[@class="bsns_pcst FL"]/span/text()').extract()
	nav =''.join(response.xpath('//span[@class="stprh colo_black"]/text()').extract())
	riskometer = ''.join(response.xpath('//div[contains(text(), "Riskometer")]//following-sibling::div/text()').extract()).strip()

	print fund
	print "%s - %s - %s - %s" %(plan, option, typ, amfi_code)
	print nav
	print riskometer     
	crisil_rank = len(response.xpath('//div/span[@class="ico_mutul icfullstar"]').extract())
	print crisil_rank
	fund_family = ''.join(response.xpath('//div[contains(text() , "FUND Family")]//following-sibling::div/a/text()').extract()).strip()
 	print fund_family
	fund_class = ''.join(response.xpath('//div[contains(text() , "FUND CLASS")]//following-sibling::div/a/text()').extract()).strip()
	print fund_class

	link = ''.join(response.xpath('//a[@title="View All Top 10 Holdings"]//@href').extract())
	yield scrapy.Request(link, callback=self.parse_2)

    def parse_2(self, response):
