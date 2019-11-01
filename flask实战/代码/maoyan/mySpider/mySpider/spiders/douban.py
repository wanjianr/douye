# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
from mySpider.items import DoubanspiderItem
import logging


logger = logging.getLogger(__name__)

class DoubanSpider(scrapy.Spider):
	name = 'douban'
	allowed_domains = ['movie.douban.com']
	start = 0
	url = 'https://movie.douban.com/top250?start='
	end = '&filter='
	start_urls = [url + str(start) + end]

	def parse(self, response):
		item = DoubanspiderItem()

		movies = response.xpath("//ol[@class='grid_view']/li")
		logger.warning('--响应成功--')
		for each in movies:

			pic_url = each.xpath('div/div[1]/a/img/@src').getall()
			# ['肖申克的救赎'，'\xa0/\xa0The Shawshank Redamption']
			title = each.xpath('div/div[2]/div[1]/a/span[1]/text() | div/div[2]/div[1]/a/span[2]/text()').getall()
			# content需要处理
			content = each.xpath('div/div[2]/div[2]/p[1]/text()').getall()
			# score = ['9.7','89979人评价']
			score = each.xpath('div/div[2]/div[2]/div/span/text()').getall()
			info = each.xpath('div/div[2]/div[2]/p[2]/span/text()').getall()
			detail_link = each.xpath('div/div[2]/div[1]/a/@href').get()

			item['pic_url'] = pic_url[0]
			item['title'] = title[0] + title[1]
			# 以;作为分隔，将content列表里所有元素合并成一个新的字符串
			item['content'] = content[0].strip().replace('\xa0\xa0\xa0',' / ') + ';' + content[1].strip().replace('\xa0','')
			item['score'] = score[0] + '/' + score[1]
			item['info'] = info[0]

			# pic_url = each.xpath('div/div[1]/a/img/@src').extract_first()
			# # ['肖申克的救赎'，'\xa0/\xa0The Shawshank Redamption']
			# title = each.xpath('div/div[2]/div[1]/a/span[1]/text() | div/div[2]/div[1]/a/span[2]/text()').extract_first()
			# # content需要处理
			# content = each.xpath('div/div[2]/div[2]/p[1]/text()').extract_first()
			# # score = ['9.7','89979人评价']
			# score = each.xpath('div/div[2]/div[2]/div/span/text()').extract_first()
			# info = each.xpath('div/div[2]/div[2]/p[2]/span/text()').extract_first()
			# detail_link = each.xpath('div/div[2]/div[1]/a/@href').extract_first()

			# item['pic_url'] = pic_url[0]
			# item['title'] = title[0] + title[1]
			# # 以;作为分隔，将content列表里所有元素合并成一个新的字符串
			# item['content'] = content[0].strip().replace('\xa0\xa0\xa0',' / ') + ';' + content[1].strip().replace('\xa0','')
			# item['score'] = score[0] + '/' + score[1]
			# item['info'] = info[0]
			# item['detail_link'] = detail_link[0]
			logger.warning('--正在抓取列表页面信息--')
			yield scrapy.Request(
				detail_link,
				callback = self.detail_page,
				meta = {'item':deepcopy(item)}
				)

		if self.start <= 225:
			self.start += 25
			yield scrapy.Request(self.url + str(self.start) + self.end, callback=self.parse)

	def detail_page(self, response):
		logger.warning('--正在抓取详情页面信息--')
		item = response.meta['item']

		intro = response.xpath('//*[@id="link-report"]/span[1]/text()').getall()

		item['intro'] = ';'.join(intro)

		yield item


		
