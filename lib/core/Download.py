#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
download html 文件
'''
import requests

headers ={
		    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
            'Referer': 'http://www.baidu.com',
            'Cookie': 'whoami=Ajatar',
		}

class Downloader(object):
    def get(self,url):
        r = requests.get(url,timeout=10,headers=headers)
        if r.status_code != 200:
            return None
        _str = r.text
        return _str

    def post(self,url,data):
        r = requests.post(url,data,headers=headers)
        _str = r.text
        return _str

    #其实还是get方式download html
    def download(self, url,htmls):
        if url is None:
            return None
        _str = {}
        _str["url"] = url
        try:
            r = requests.get(url, timeout=10,headers=headers)
            if r.status_code != 200:
                return None
            _str["html"] = r.text
        except Exception as e:
            return None
        htmls.append(_str)