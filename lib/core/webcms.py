#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
cms区分py
'''

import json,os,sys,hashlib,threading,Queue,re
from lib.core import Download
from lib.core import outputer
output = outputer.outputer()

class webcms(object):
    workQueue = Queue.Queue()
    URL = ""
    threadNum = 0
    NotFound = True
    Downloader = Download.Downloader()
    result = ""

    def __init__(self,url,threadNum = 10):
        self.URL = url
        self.threadNum = threadNum
        filename = os.path.join(sys.path[0], "data", "cmsdata.json")
        fp = open(filename)
        #load json数据
        webdata = json.load(fp,encoding="utf-8")
        for i in webdata:
            self.workQueue.put(i)
        fp.close()
    
    #生成md5函数
    def getmd5(self, body):
        m2 = hashlib.md5()
        m2.update(body)
        return m2.hexdigest()

    def th_whatweb(self):
    	#data数据没用cns
        if(self.workQueue.empty()):
            self.NotFound = False
            return False

        if(self.NotFound is False):
            return False
        cms = self.workQueue.get()
        #url+url特征
        _url = self.URL + cms["url"]
        #download html 
        html = self.Downloader.get(_url)
        print "[whatweb log]:checking %s"%_url
        if(html is None):
            return False
        #根据re判断
        if cms["re"]:
            if(html.find(cms["re"])!=-1):
                self.result = cms["name"]
                self.NotFound = False
                return True
        else:#根据md5判断
            md5 = self.getmd5(html)
            if(md5==cms["md5"]):
                self.result = cms["name"]
                self.NotFound = False
                return True
    
    def run(self):
    	#以Notfound判断是否继续循环，即是否找到cms
        while(self.NotFound):
            th = []
            for i in range(self.threadNum):
            	#线程函数th_whatweb
                t = threading.Thread(target=self.th_whatweb)
                t.start()
                th.append(t)
            for t in th:
                t.join()
        #是否找到cms
        if(self.result):
            print "[webcms]:%s cms is %s"%(self.URL,self.result)
            output.add("Webcms","[webcms]:%s cms is %s"%(self.URL,self.result))
        else:
            print "[webcms]:%s cms NOTFound!"%self.URL
            output.add("Webcms","[webcms]:%s cms NOTFound!"%(self.URL))