# -*- coding: utf-8 -*-
import scrapy
from mySpider.items import AllBookspiderItem
import logging
from copy import deepcopy
import re

logger = logging.getLogger(__name__)

class AllCategorySpider(scrapy.Spider):
	name = 'all_category'
	allowed_domains = ['bang.dangdang.com']
	start_urls = ['http://bang.dangdang.com/books/bestsellers/01.41.70.00.00.00-month-2019-7-2-1']

	def parse(self, response):
		# 获取start_urls响应，并提取所有类别图书地址
		category_list = response.xpath('//*[@id="sortRanking"]/div[@class="side_nav"]/a') 
		for each in category_list:
			item = AllBookspiderItem()
			item['category'] = each.xpath('text()').get() # 获取相应类型名
			url = each.xpath('@href').get()               # 获取对应类型的url
			yield scrapy.Request(
				url,
				callback = self.subcategroy,
				meta = {'item':deepcopy(item)}
				)

	def subcategroy(self, response):
		item = response.meta['item']
		subcategroy_list = response.xpath('//*[@id="sortRanking"]/ul/li')
		for each in subcategroy_list:
			item['sub_category'] = each.xpath('a/text()').get() # 获取子类名称
			url = each.xpath('a/@href').get()                   # 获取子类url

			yield scrapy.Request(
				url,
				callback = self.save_book,
				meta = {'item':deepcopy(item)}
				)

		current_page = int(re.findall(r'<span class="or">(.*?)</span>', response.text)[0])
		total_page = int(re.findall(r'<span class="or">.*?</span>.*?<span>/(.*?)</span>', response.text, re.S)[0])
		logger.info(current_page)
		logger.info(total_page)
		if current_page < total_page:
			url_temp = re.findall(r'(.*?2019-7-2-).*?',response.request.url)[0]
			url = url_temp + str(current_page+1)
			logger.warning(url)
			yield scrapy.Request(
				url = url,
				callback = self.subcategroy,
				meta = {'item':item}
			)

	def save_book(self, response):
		item = response.meta['item']
		for each in response.xpath('//ul[@class="bang_list"]/li'):
			item['book_name'] = each.xpath('div[3]/a/text()').get()
			item['book_rank'] = each.xpath('div[1]/text()').get()
			item['price'] = each.xpath('div[7]/p[1]/span[1]/text()').get()
			item['writer'] = each.xpath('div[5]/a[1]/@title').get()
			item['pic_url'] = each.xpath('div[2]/a/@href').get()

			yield item