import scrapy
import re, MySQLdb


class MoneycontrolSpider(scrapy.Spider):
    name = "moneycontrol"
    allowed_domains = ["www.moneycontrol.com"]
    start_urls = (
        'http://www.moneycontrol.com/',
    )
   
    def __init__(self, *args, **kwargs):
        super(MoneycontrolSpider, self).__init__(*args, **kwargs)
        #self.conn = MySQLdb.connect(db='PROJECT_1', host= '10.28.218.81', user='veveo', passwd='veveo123', charset='utf8', use_unicode=True)
        self.conn=MySQLdb.connect(db='MINE',host='localhost',user='root', passwd ='malini.123', charset='utf8',use_unicode=True)
        self.cursor = self.conn.cursor()

    def parse(self, response):
        stock=response.xpath('//div[@class="flS2"]/a[contains(@href,"stockpricequote")]')
	for i in stock:
		stock_links=i.xpath('.//@href').extract_first()
		#if 'https://www.moneycontrol.com/india/stockpricequote/Z' in stock_links:
		yield scrapy.Request(stock_links, self.parse_page1)
   
    def parse_page1(self,response):
	stock_alphabets=response.xpath('//td/a')
	for j in stock_alphabets:
		alphabet_links=j.xpath('.//@href').extract_first()
		print alphabet_links
		yield scrapy.Request(alphabet_links, self.parse_page2)


    def parse_page2(self,response):
	company_name=response.xpath('//div[@class="b_42 MB10 PT5 PR"]/h1/text()').extract()
	bse_price=response.xpath('//span[@id="Bse_Prc_tick"]//text()').extract()
	nse_price=response.xpath('//span[@id="Nse_Prc_tick"]//text()').extract()
	company_name=''.join(company_name).strip()
	bse_price=''.join(bse_price).strip()
	nse_price=''.join(nse_price).strip()
	if len(company_name)!=0:
		query = "insert into moneyctrl(company_name,bse_price,nse_price,created_at,modified_at)"
        	query += 'values(%s, %s, %s, now(), now())on duplicate key update modified_at = now()'
		if bse_price == '':
			bse_price = None
		if nse_price == '':
			nse_price = None
        	values = (str(company_name), bse_price, nse_price)
		try:
        		self.cursor.execute(query,values)
		except:
			import pdb;pdb.set_trace()

    def spider_closed(self, spider):

        self.cursor.close()
        self.conn.close()


