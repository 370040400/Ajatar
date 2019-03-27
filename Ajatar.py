#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Name:Ajatar
Author: jf
Copyright (c) 2019
'''

import sys,argparse,os,inspect
from lib.core.Spider import SpiderMain
from lib.core import webcms,common,PortScan,webdir,outputer,fun_until
from lib.core.settings import IS_WIN
from lib.core.option import initOption
from lib.core.data import logger, paths
from lib.utils.configfile import configFileParser
#thirdparty 还没分析直接用了别人的 又线程池那些东东- -
from thirdparty.colorama.initialise import init as windowsColorInit #Windows界面颜色

sys.dont_write_bytecode = True  # 不生成pyc文件

try:
	# this has to be the first non-standard import
	__import__("lib.utils.versioncheck")
except ImportError:
	exit("[!] wrong installation detected (missing modules). Please install python version for 2.7.x")


def modulePath():
	"""
    This will get us the program's directory, even if we are frozen
    using py2exe
    """
	try:
		#sys.executable 返回的是py2.exe的路径，__file__ 该文件路径
		_ = sys.executable if weAreFrozen() else  __file__
	except NameError:
		#获得当前文件路径 相当于__file__
		_ = inspect.getsourcefile(modulePath)
	#os.path.dirnane....获取py2.exe上一层文件路径
	#sys.getfilesystemencoding() 获取文件系统使用编码方式，Windows下返回'mbcs'，mac下返回'utf-8'
	return common.getUnicode(os.path.dirname(os.path.realpath(_)),encoding=sys.getfilesystemencoding())

def checkEnvironment():
	try:
		os.path.isdir(modulePath()) #os.path.isdir()用于判断对象是否为一个目录
	except UnicodeEncodeError:
		errMsg = "your system does not properly handle non-ASCII paths. "
		errMsg += "Please move the Ajatar's directory to the other location"
		logger.critical(errMsg)
		raise SystemExit

def main():
	checkEnvironment()#检测环境
	common.setPaths(modulePath())# 为一些目录和文件设置了绝对路径

	#目标url，一些参数设置
	parser = argparse.ArgumentParser(description="Ajatar scan must a url")
	parser.add_argument("-u","--url",help="url")
	args = parser.parse_args()
	root = args.url
	#root = "http://www.imufe.edu.cn/"

	#判断是否为Windows
	if IS_WIN:
		#Windows界面颜色
		windowsColorInit()
	#Banner()

	try:
		configFileParser(os.path.join(paths.Ajatar_ROOT_PATH,"config.conf"))
		#线程数
		threadNum = initOption(args)
	except Exception as e:
		raise e

	#拆解url 得到netloc
	domain = common.Ajurlparse(root)
	#输出报告对象
	output = outputer.outputer()

	# CDN Check
	print "CDN check...."
	iscdn = True
	try:
		msg,iscdn =  fun_until.checkCDN(root)
		#获取数据生成报告
		output.add("cdn",msg)
		#build html
		output.build_html(domain)
		print msg
	except:
		print "[Error]:CDN check error"

	if iscdn:
		#IP Ports Scan
		#获取ip
		ip = common.gethostbyname(root)
		print "IP:",ip
		print "Start Port Scan:"
		#ip端口扫描
		pp = PortScan.PortScan(ip)
		pp.work()
		output.build_html(domain)

	# DIR Fuzz
	dd = webdir.webdir(root,threadNum)
	dd.work()
	dd.output()
	output.build_html(domain)

	#webcms
	ww = webcms.webcms(root,threadNum)
	ww.run()
	output.build_html(domain)

	#spider
	Aj = SpiderMain(root,threadNum)
	Aj.craw()

if __name__ == '__main__':
	main()