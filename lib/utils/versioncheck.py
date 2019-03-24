#!/usr/bin/env python

import sys
PYVERSION = sys.version.split()[0]

if PYVERSION >= "3" or PYVERSION < "2.6":
	exit("[CRITICAL] incompatible Python version detected ('%s'). For successfully running sqlmap you'll have to use version 2.6.x or 2.7.x (visit 'http://www.python.org/download/')" % PYVERSION)