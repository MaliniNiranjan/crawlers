import scrapy
import re, MySQLdb

class ZigwheelSpider(scrapy.Spider):
    name = "zigwheel"
    allowed_domains = ['www.zigwheels.com']
    start_urls = ['http://www.zigwheels.com/top-selling-cars/']

    def __init__(self, *args, **kwargs):
        super(ZigwheelSpider, self).__init__(*args, **kwargs)
        #self.conn = MySQLdb.connect(db='PROJECT_1', host= '10.28.218.81', user='veveo', passwd='veveo123', charset='utf8', use_unicode=True)
        self.conn=MySQLdb.connect(db='MINE',host='localhost',user='root', passwd ='malini.123', charset='utf8',use_unicode=True)
        self.cursor = self.conn.cursor()

    '''def spider_closed(self, spider):
        self.cursor.close()
        self.conn.close()'''


    def parse(self, response):
	car=response.xpath('//div[@class="col-sm-6 p-15 deviceCenter m-pb-0 m-pt-0"]/a')
	for i in car:
		car_links=i.xpath('./@href').extract_first()
                car_links="https://www.zigwheels.com" + car_links
                yield scrapy.Request(car_links, self.parse_page1)

    def parse_page1(self,response):
	car_name=response.xpath('//div//h1//text()').extract()
        rating=response.xpath('//div[@class="r-w fnt-12 rel i-b mr-5"]/text()').extract()
        price=response.xpath('//span[@itemprop="offers"]/text()').extract()
        for i in range(len(price)):
		if len(price[i].strip())!=0:
			price=price[i].strip().split('-')


        max_price=price[1]
	max_price=max_price.strip().replace('lakh','')

        min_price=price[0]
        min_price=min_price.replace("Rs. ","") 
	car_name=''.join(car_name).strip()
        rating=''.join(rating)
        yield {'Car_name': car_name,
               #'Ratings': rating,
        	'Min_price': min_price,
        	'Max_price': max_price}
	#import pdb;pdb.set_trace()

	query = 'insert into zigwheel(car_name, rating, min_price, max_price, created_at, modified_at)'
	query += 'values(%s,%s,%s,%s, now(), now())on duplicate key update modified_at = now()'
    	values = (str(car_name),str(rating),str(min_price),str(max_price))
    	self.cursor.execute(query,values)

    def spider_closed(self, spider):

	self.cursor.close()
        self.conn.close()


