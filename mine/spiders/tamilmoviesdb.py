# -*- coding: utf-8 -*-
import scrapy


class TamilmoviesdbSpider(scrapy.Spider):
    name = "tamilmoviesdb"
    allowed_domains = ["tamilmoviesdatabase.com"]
    start_urls = (
        'http://www.tamilmoviesdatabase.com/movies/',
    )

    def parse(self, response):
        moviedetails = response.xpath('//div[@class="row margin-bottom"]//div[@class="movie-name"]/h4')
	for i in moviedetails:
		moviename = i.xpath('.//a/text()').extract()
		moviename = ''.join(moviename)
		movielink = i.xpath('.//a/@href').extract()
		movielink =''.join(movielink)	
		yield scrapy.Request(movielink,self.parse_page1 ,meta={'moviename': moviename})

	if "flag" not in response.meta.keys():
		for j in range(2,303):
			next_page = 'http://tamilmoviesdatabase.com/movies/page/%s/' %j
			yield scrapy.Request(next_page, self.parse, meta={'flag' : True})		

    def parse_page1(self,response):
	release_yr = response.xpath('//div[@class="moview-info"]/div/h1/text()').extract_first()
	release_yr = release_yr.strip().split('(')
	release_yr = release_yr[1]. replace(')' , '')
	#print release_yr
	genre = response.xpath('//div[@class="moview-info"]/div/span/text()').extract_first()
	rating =response.xpath('//div[@class="rating-star"]/span[@class="moviedb-rating-summary"]/text()').extract_first()
	rating = rating.split('/')
	rating=rating[0]
	#import pdb; pdb.set_trace();
	director=response.xpath('//div[@class="details-wrapper"]/ul/li[@class="director"]/a/text()').extract_first()
	director_link =response.xpath('//div[@class="details-wrapper"]/ul/li[@class="director"]/a/@href').extract_first()
	actors= response.xpath('//div[@class="details-wrapper"]/ul/li[@class="actors"]/a/text()').extract()
	actors_link=response.xpath('//div[@class="details-wrapper"]/ul/li[@class="actors"]/a/@href').extract()
	actors = ','.join(actors)
	#release_date = response.xpath('//li[@class="common-list"]/text()').extract_first()
	#release_date= release_date[0]
	print release_yr
	print genre
	print rating
	print director
	print actors
	#print release_date
	moviename =response.meta['moviename']
	yield{'Moviename' :moviename ,'Release_yr' :release_yr , 'Genres' : genre ,'Rating' :rating ,'Director' :  director ,'Actors' :actors}
