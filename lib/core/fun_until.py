#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
CND判断py文件
'''

import requests
import re
import time
import urlparse
from lib.core import common

def _get_static_post_attr(page_content):
    """
    Get params from <input type='hidden'>

    :param page_content:html-content
    :return dict contains "hidden" parameters in <form>
    """
    _dict = {}
    # soup = BeautifulSoup(page_content, "html.parser")
    # for each in soup.find_all('input'):
    #     if 'value' in each.attrs and 'name' in each.attrs:
    #         _dict[each['name']] = each['value']

    #获得第二次post数据
    _dict["type"] = "get"
    _dict["__token__"] = common.GetMiddleStr(page_content,'<input type="hidden" name="__token__" value="','" /></form>')

    return _dict

def checkCDN(url):
    """
    Detect if the website is using CDN or cloud-based web application firewall

    :param url: Target URL or Domain
    :return True / False
    """
    #拆分url得到netloc
    url = common.Ajurlparse(url)

    #cdn判断网址
    dest = 'http://ce.cloud.360.cn/'

    #生成sesiion 方便多次post
    s = requests.session()

    #得到第二次post的字典
    data1 = _get_static_post_attr(s.get(dest).content)
    data1['domain'] = url
    #共三个参数，domin:url,type:get,token:xxx
    s.post('http://ce.cloud.360.cn/task', data=data1)

    #设置头部
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    s.post('http://ce.cloud.360.cn/Tasks/detect', data=data1, headers=headers)

    time.sleep(5)  # 5 sec delay for nodes to detect

    #第三次post数据
    data = 'domain=' + url + '&type=get&ids%5B%5D=1&ids%5B%5D=2&ids%5B%5D=3&ids%5B%5D=4&ids%5B%5D=5&ids%5B%5D=6&ids%5B%5D=7&ids%5B%5D=8&ids%5B%5D=9&ids%5B%5D=16&ids%5B%5D=18&ids%5B%5D=22&ids%5B%5D=23&ids%5B%5D=41&ids%5B%5D=45&ids%5B%5D=46&ids%5B%5D=47&ids%5B%5D=49&ids%5B%5D=50&ids%5B%5D=54&ids%5B%5D=57&ids%5B%5D=58&ids%5B%5D=61&ids%5B%5D=62&ids%5B%5D=64&ids%5B%5D=71&ids%5B%5D=78&ids%5B%5D=79&ids%5B%5D=80&ids%5B%5D=93&ids%5B%5D=99&ids%5B%5D=100&ids%5B%5D=101&ids%5B%5D=103&ids%5B%5D=104&ids%5B%5D=106&ids%5B%5D=110&ids%5B%5D=112&ids%5B%5D=114&ids%5B%5D=116&ids%5B%5D=117&ids%5B%5D=118&ids%5B%5D=119&ids%5B%5D=120&ids%5B%5D=121&ids%5B%5D=122&user_ip_list='
    r = s.post('http://ce.cloud.360.cn/GetData/getTaskDatas', data=data, headers=headers)

    #ping的ip数
    ips = re.findall('"ip":"(.*?)"', r.content)
    #去除相同ip 利用set集合
    ans = list(set(ips))
    msg = url

    #Target错误时
    if not len(ips):
        msg += ' [Target Unknown]'
        return msg,False
    #ip不唯一，即有CDN
    msg += ' [CDN Found!]' if len(ans) > 1 else ''
    msg += ' Nodes:' + str(len(ips))
    msg += ' IP(%s):' % str(len(ans)) + ' '.join(ans)
    return msg,True