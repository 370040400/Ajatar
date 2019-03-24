#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
端口扫描py
'''

import socket
import threading
import Queue
from lib.core import outputer
output = outputer.outputer()

class PortScan:
	def __init__(self,ip="locallhost",threadNum=5):
		self.PORT = {80:"web",8080:"web",3311:"kangle",3312:"kangle",3389:"mstsc",4440:"rundeck",5672:"rabbitMQ",5900:"vnc",6082:"varnish",7001:"weblogic",8161:"activeMQ",8649:"ganglia",9000:"fastcgi",9090:"ibm",9200:"elasticsearch",9300:"elasticsearch",9999:"amg",10050:"zabbix",11211:"memcache",27017:"mongodb",28017:"mondodb",3777:"dahua jiankong",50000:"sap netweaver",50060:"hadoop",50070:"hadoop",21:"ftp",22:"ssh",23:"telnet",25:"smtp",53:"dns",123:"ntp",161:"snmp",8161:"snmp",162:"snmp",389:"ldap",443:"ssl",512:"rlogin",513:"rlogin",873:"rsync",1433:"mssql",1080:"socks",1521:"oracle",1900:"bes",2049:"nfs",2601:"zebra",2604:"zebra",2082:"cpanle",2083:"cpanle",3128:"squid",3312:"squid",3306:"mysql",4899:"radmin",8834:'nessus',4848:'glashfish'}
		self.threadNum = threadNum
		self.q = Queue.Queue()
		self.ip = ip
		for port in self.PORT.keys():
			self.q.put(port)

	def _th_scan(self):
		#判断队列是否为空，即扫描端口是否完成
		while not self.q.empty():
			#先进先出
			port = self.q.get()
			
# TCP端口扫描一般分为以下几种类型：
# TCP connect扫描：也称为全连接扫描，这种方式直接连接到目标端口，完成了TCP三次握手的过程，这种方式扫描结果比较准确，但速度比较慢而且可轻易被目标系统检测到。
# TCP SYN扫描：也称为半开放扫描，这种方式将发送一个SYN包，启动一个TCP会话，并等待目标响应数据包。如果收到的是一个RST包，则表明端口是关闭的，而如果收到的是一个SYN/ACK包，则表示相应的端口是打开的。
# Tcp FIN扫描：这种方式发送一个表示拆除一个活动的TCP连接的FIN包，让对方关闭连接。如果收到了一个RST包，则表明相应的端口是关闭的。
# TCP XMAS扫描：这种方式通过发送PSH、FIN、URG、和TCP标志位被设为1的数据包。如果收到了一个RST包，则表明相应的端口是关闭的。

			#Tcp方式探测,AF_INET 表示用IPV4地址族,SOCK_STREAM 是说是要是用流式套接字
			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.settimeout(1)
			try:
				s.connect((self.ip,port))
				print "%s:%s OPEN [%s]"%(self.ip,port,self.PORT[port])
				output.add_list("PortScan","%s:%s OPEN [%s]"%(self.ip,port,self.PORT[port]))
			except:
				print "%s:%s Close"%(self.ip,port)
				output.add_list("PortScan","%s:%s Close"%(self.ip,port))
			finally:
				s.close()

	#工作函数
	def work(self):
		threads = []
		for i in range(self.threadNum):
			#线程函数_th_scan
			t = threading.Thread(target=self._th_scan())
			threads.append(t)
			t.start()
		for t in threads:
			t.join()
		print('[*] The scan is complete!')
