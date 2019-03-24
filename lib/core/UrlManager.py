#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
url管理文件
'''
class UrlManager(object):
	def __init__(self):
		self.new_urls = set()
		self.old_urls = set()

	#添加 url 到 新url集合
	def add_new_url(self,url):
		if url is None:
			return
		if url not in self.new_urls and url not in self.old_urls:
			self.new_urls.add(url)

	#添加 url群 到 新url集合
	def add_new_urls(self,urls):
		if urls is None or len(urls) == 0:
			return
		for url in urls:
			self.add_new_url(url)

	#判断 新url集合 中是否还有目标
	def has_new_url(self):
		return len(self.new_urls) !=0

	# 从 新url集合 中pop 弹出一个url进行检测 并加入到 旧url集合 中
	def get_new_url(self):
		new_url = self.new_urls.pop()
		self.old_urls.add(new_url)
		return str(new_url)
