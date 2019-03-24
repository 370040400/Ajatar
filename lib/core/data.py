#!/usr/bin/env python

"""
Copyright (c) 2006-2017 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
from lib.core.datatype import AttribDict
from lib.core.log import MY_LOGGER

logger = MY_LOGGER

# Ajatar paths
paths = AttribDict()

# Ajatar cmder
cmdLineOptions = AttribDict()

# Ajatar urlconfig
urlconfig = AttribDict()
Ajconfig = AttribDict()

# Ajatar plugins pycode hash
Aj_hash_pycode = dict()