# -*- coding: utf-8 -*-
import scrapy
import re, MySQLdb



class MutualfundsSpider(scrapy.Spider):
    name = "mutualfunds_1"
    start_urls = (
        'https://www.moneycontrol.com/',
    )
    
    def __init__(self, *args, **kwargs):
        super(MutualfundsSpider, self).__init__(*args, **kwargs)
        self.conn=MySQLdb.connect(db='MINE',host='localhost',user='root', passwd ='malini.123', charset='utf8',use_unicode=True)
        self.cursor = self.conn.cursor()


    def parse(self, response):
        fundlink= response.xpath('//a[contains(@href ,"mutualfunds")]')
	for i in fundlink:
		fundlink1=''.join(i.xpath('.//@href').extract())
		yield scrapy.Request(fundlink1,self.parse_page)
	
    def parse_page(self ,response):
	flink = response.xpath('//td/a[contains(@href ,"mutual-funds")]')
	for i in flink:
		flink1 = "https://www.moneycontrol.com"+''.join(i.xpath('.//@href').extract())
		yield scrapy.Request(flink1 , self.parse_page1)

    def parse_page1(self , response):
	fund = ''.join(response.xpath('//h1[@class="pcstname"]/text()').extract()).strip()
	plan_list = ''.join(response.xpath('//div/div[@class="bsns_pcst FL"]//text()').extract())
	Plan_details={}
	plan_list = plan_list.split('|')
	for i in plan_list:
		i=i.strip().split(':')
		Plan_details[i[0].strip()] = i[1].strip()
        crisil_rank = len(response.xpath('//div/span[@class="ico_mutul icfullstar"]').extract())
        fund_family = ''.join(response.xpath('//div[contains(text() , "FUND Family")]//following-sibling::div/a/text()').extract()).strip()
        fund_class = ''.join(response.xpath('//div[contains(text() , "FUND CLASS")]//following-sibling::div/a/text()').extract()).strip()
        link  = ''.join(response.xpath('//a[@title="View All Top 10 Holdings"]//@href').extract()).split('/')
	sk = link[-1]
	url = ''.join(response.xpath('//a[@title="View All Top 10 Holdings"]//@href').extract())
	
	riskometer = ''.join(response.xpath('//div[contains(text(), "Riskometer")]//following-sibling::div/text()').extract()).strip()
	nav =''.join(response.xpath('//span[@class="stprh colo_black"]/text()').extract())

	print sk 
	print url
	#print fund_family
	#print response.url
	#print plan_list
	#print option
	#print Type
	#print Amfi_code
        #print fund
        #print plan
        #print nav
        #print riskometer
        #print crisil_rank
        #print fund_class
	#print link 
	#print'\n'
       	data = {"fund_family" :fund_family , "fund_name" :fund,
		"crisil_rank" :crisil_rank , "riskometer" :riskometer , "nav_point" : nav ,
		 "fund_class" : fund_class}
	data.update(Plan_details)
	
	query = "insert into mutalfunds(sk,queue,status)"
        query += 'values(%s, %s, %s)'
	values = (sk,url,0)
	self.cursor.execute(query,values)
	self.conn.commit()
	yield data

    def spider_closed(self, spider):
	self.cursor.close()
        self.conn.close()
