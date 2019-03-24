#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
敏感目录爆破py
'''

import os,sys,Queue,requests,threading
from lib.core import outputer
output = outputer.outputer()

class webdir:
	def __init__(self,root,threadNum):
		self.root = root
		self.threadNum = threadNum
		self.headers = {
		    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
            'Referer': 'http://www.baidu.com',
            'Cookie': 'whoami=Ajatar',
		}
		self.task = Queue.Queue()
		self.s_list = []
		filename = os.path.join(sys.path[0],"data","dir.txt")
		for line in open(filename):
			self.task.put(root + line.strip())

	def checkdir(self,url):
		status_code = 0
		try:
			r = requests.head(url,headers=self.headers)
			status_code = r.status_code
		except:
			status_code = 0
		return status_code

	def test_url(self):
		#判断队列是否为空
		while not self.task.empty():
			url = self.task.get()
			#检测url是否live
			s_code = self.checkdir(url)
			#状态码为200即live
			if s_code==200:
				self.s_list.append(url)
				#报告生成以列表
				output.add_list("Web_Path",url)
			print "Testing: %s status:%s"%(url,s_code)

	def work(self):
		threads = []
		for i in range(self.threadNum):
			#线程函数 test_url
			t = threading.Thread(target=self.test_url())
			threads.append(t)
			t.start()
		for t in threads:
			t.join()
		print('[*]The DirScan is complete!')

	def output(self):
		#输出状态码为200的目录
		if len(self.s_list):
			print "[*] status = 200 dir:"
			for url in self.s_list:
				print url