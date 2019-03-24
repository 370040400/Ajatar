#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
通用函数py文件
'''

import socket,urlparse,os
from lib.core.settings import INVALID_UNICODE_CHAR_FORMAT
from lib.core.data import paths,logger

#url拆分出参数 这里还只用于xss插件的利用
def urlsplit(url):
    domain = url.split("?")[0]
    _url = url.split("?")[-1]
    pararm = {}
    for val in _url.split("&"):
        pararm[val.split("=")[0]] = val.split("=")[-1]

    #combine
    urls = []
    for val in pararm.values():
        new_url = domain + _url.replace(val,"my_Payload")
        urls.append(new_url)
    return urls

#根据url的netloc得到ip
def gethostbyname(url):
    domain = urlparse.urlparse(url)
    # domain.netloc
    if domain.netloc is None:
        return None
    ip = socket.gethostbyname(domain.netloc)
    return ip

#url拆出netloc
def Ajurlparse(url):
    domain = urlparse.urlparse(url)
    # domain.netloc
    if domain.netloc is None:
        return None
    return domain.netloc

#CDN的利用，拼接token，返回去post    
def GetMiddleStr(content,startStr,endStr):
    startIndex = content.index(startStr)
    if startIndex>=0:
        startIndex += len(startStr)
    endIndex = content.index(endStr)
    return content[startIndex:endIndex]

def weAreFrozen():
    """
    Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located.
    Reference: http://www.py2exe.org/index.cgi/WhereAmI
    """
    return hasattr(sys,"frozen")

def getUnicode(value, encoding=None, noneToNull=False):
    """
    Return the unicode representation of the supplied value:

    >>> getUnicode(u'test')
    u'test'
    >>> getUnicode('test')
    u'test'
    >>> getUnicode(1)
    u'1'
    """

    if noneToNull and value is None:
        return "NULL"

    if isinstance(value, unicode):#用来判断是否为unicode
        return value
    elif isinstance(value, basestring):#用来判断是否为str
        while True:
            try:
                return unicode(value, encoding or "utf8")
            except UnicodeDecodeError, ex:
                try:
                    return unicode(value, "utf8")
                except:
                    value = value[:ex.start] + "".join(INVALID_UNICODE_CHAR_FORMAT % ord(_) for _ in value[ex.start:ex.end]) + value[ex.end:]
    elif isListLike(value):
        value = list(getUnicode(_, encoding, noneToNull) for _ in value)
        return value
    else:
        try:
            return unicode(value)
        except UnicodeDecodeError:
            return unicode(str(value), errors="ignore")  # encoding ignored for non-basestring instances

def isListLike(value):
    """
    Returns True if the given value is a list-like instance

    >>> isListLike([1, 2, 3])
    True
    >>> isListLike(u'2')
    False
    """

    return isinstance(value, (list, tuple, set))

def setPaths(rootPath):
	"""
	Sets abolute paths for project directoies and files
	"""

	paths.Ajatar_ROOT_PATH = rootPath

	#Ajatar pahts
	paths.Ajatar_Plugin_Path = os.path.join(paths.Ajatar_ROOT_PATH,"plugins")
	paths.Ajatar_Output_Path = os.path.join(paths.Ajatar_ROOT_PATH, "output")