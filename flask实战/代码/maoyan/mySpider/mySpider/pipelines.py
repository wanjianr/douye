# -*- coding: utf-8 -*-
import json
import logging
import pymysql

logger = logging.getLogger(__name__)
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
class MyspiderPipeline(object):

	def open_spider(self, spider):
		if spider.name == 'dangdang':
			logger.warning('--爬取当当网--')
			self.file = open('book.json','w',encoding='utf-8')
		elif spider.name == 'itcast':
			logger.warning('--爬取教师信息--')
			self.file = open('teacher.json','w',encoding='utf-8')
		elif spider.name == 'all_category':
			logger.warning('--爬取当当网所有类型数据的top100--')
			self.file = open('all_category.json','w',encoding='utf-8')
		elif spider.name == 'douban':
			logger.warning('--爬取豆瓣网top250的电影--')
			self.file = open('douban.json','w',encoding='utf-8')
		elif spider.name == 'maoyan':
			logger.warning('--爬取top100的电影--')
			self.file = open('maoyan.json','w',encoding='utf-8')

	def process_item(self, item, spider):
		content = json.dumps(dict(item), ensure_ascii=False) + '\n'
		logger.warning('--正在保存图书信息...--')
		self.file.write(content)
		return item

	def close_spider(self, spider):
		self.file.close()

class MysqlPipeline(object):
	def __init__(self):
		#链接数据库
		self.connect = pymysql.connect(
			# host = spider.settings.get('MYSQL_HOST'),#数据库地址
			# port = spider.settings.get('MYSQL_PORT'),#数据库端口
			# db = spider.settings.get('MYSQL_DBNAME'),#数据库名称
			# user = spider.settings.get('MYSQL_USER'),#数据库用户名
			# passwd = spider.settings.get('MYSQL_PASSWORD'),#数据库密码
			# charset = spider.settings.get('MYSQL_CHARSET'),#数据库编码
			host = 'localhost',#数据库地址
			port = 3306,#数据库端口
			db = 'flaskweb',#数据库名称
			user = 'root',#数据库用户名
			passwd = 'password',#数据库密码
			charset = 'utf8',#数据库编码
			use_unicode = True
		)
		#拿到操作数据库的游标
		self.cursor = self.connect.cursor()

	def process_item(self,item,spider):
		sql = "insert into maoyan(id,rank,pic_url,name,actors,time,intro,site,prize_url,prize_name,prize_content) values(0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		data = (item['rank'],item['pic_url'],item['name'],item['actors'],item['time'],item['intro'],item['site'],item['prize_url'],item['prize_name'],item['prize_content'])
		self.cursor.execute(sql,data)
		#提交sql
		self.connect.commit()
		logger.warning('----数据更新成功----')
		return item

	def close_spider(self, spider):
		self.cursor.close()
		self.connect.close()


class PrintItemPipeline(object):
	def process_item(self, item, spider):
		logger.warning('---------------------------------------------------')
		logger.warning(item['rank'])
		logger.warning(item['pic_url'])
		logger.warning(item['name'])
		logger.warning(item['actors'])
		logger.warning(item['time'])
		# logger.warning(item['pic_url'])
		# logger.warning(item['title'])
		# logger.warning(item['content'])
		# logger.warning(item['score'])
		# logger.warning(item['info'])
		# logger.warning(item['intro'])
		return item
