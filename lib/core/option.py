#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import os
import logging
import time
from lib.core.data import paths,logger,urlconfig,Ajconfig
#from lib.core.common import makeurl,printMessage
from lib.core.settings import LIST_PLUGINS
from lib.core.enums import CUSTOM_LOGGING
from lib.core.log import LOGGER
from lib.core.exception import ToolkitUserQuitException
from lib.core.exception import ToolkitMissingPrivileges
from lib.core.exception import ToolkitSystemException

def initOption(args):
	urlconfig.mutiurl = False
	urlconfig.url = []
	urlconfig.search = False
	urlconfig.usePlugin = False

	#初始化配置文件的选项
	urlconfig.threadNum = Ajconfig.threadNum
	if urlconfig.threadNum is None:
		urlconfig.threadNum = 5
	urlconfig.deepMax = Ajconfig.crawlerDeep
	if urlconfig.deepMax is None:
		urlconfig.deepMax = 100

	urlconfig.threadNum = int(urlconfig.threadNum)
	urlconfig.deepMax = int(urlconfig.deepMax)

	return urlconfig.threadNum


