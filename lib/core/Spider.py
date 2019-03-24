#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
爬虫py
'''
import sys
import plugin
from lib.core import Download,UrlManager,common
import threading
from urlparse import urljoin
from bs4 import BeautifulSoup
from lib.core import outputer

reload(sys) 
sys.setdefaultencoding('utf8')
output = outputer.outputer()

class SpiderMain(object):
    def __init__(self,root,threadNum):
        self.urls = UrlManager.UrlManager()
        self.download = Download.Downloader()
        self.root = root
        self.threadNum = threadNum

    #判断是否为得到的新url 为root 
    def _judge(self, domain, url):
        if (url.find(domain) != -1):
            return True
        else:
            return False

    #传入html  并生成soup解析器
    def _parse(self,page_url,content):
        if content is None:
            return
        soup = BeautifulSoup(content, 'html.parser')
        _news = self._get_new_urls(page_url,soup)
        return _news

    #根据 a 标签 的href属性得到新的 url(root+url) 
    def _get_new_urls(self, page_url,soup):
        new_urls = set()
        links = soup.find_all('a')
        for link in links:
            new_url = link.get('href')
            #url(root+url) 
            new_full_url = urljoin(page_url, new_url)
            #判断是否相同url
            if(self._judge(self.root,new_full_url)):
                new_urls.add(new_full_url)
        return new_urls

    def craw(self):
    	#首先添加的是目标url到 新url集合 里 
        self.urls.add_new_url(self.root)
        #has_new_url 在UrlManager文件 判断 新url集合 是否还有目标
        while self.urls.has_new_url():
            _content = []
            th = []
            for i in list(range(self.threadNum)):
                if self.urls.has_new_url() is False:
                    break
                #从 新url集合 中pop出url
                new_url = self.urls.get_new_url()

                ##sql check
                # try:
                #     if(sqlcheck.sqlcheck(new_url)):
                #         print("url:%s sqlcheck is valueable"%new_url)
                #     except:
                #         pass
                print("craw:" + new_url)
                #报告以列表
                output.add_list("path_craw",new_url)
                output.build_html(common.Ajurlparse(self.root))
                #调用 Download文件 _content 即 download 函数中的 html
                t = threading.Thread(target=self.download.download,args=(new_url,_content))
                t.start()
                th.append(t)
            for t in th:
                t.join()
            for _str in _content:
                if _str is None:
                    continue
                # _parse 爬取每个页面 a中的 url
                new_urls = self._parse(new_url,_str["html"])

                #不用的插件
                disallow = ["sqlcheck","xss_check","bak_check"]#"要用时去掉 sqlcheck","xss_check","bak_check"
                #动态 __import__ 调用插件
                _plugin = plugin.spiderplus("script",disallow)
                # url,html即 _content中的
                _plugin.work(_str["url"],_str["html"])

                #循环添加 爬虫就是这样
                self.urls.add_new_urls(new_urls)