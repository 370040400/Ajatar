# -*- coding:utf-8 -*-
a = "你好，world"
a = a.decode("utf-8").encode("gb2312")
print a
import sys
import os
import inspect

import subprocess
# Format used for representing invalid unicode characters
INVALID_UNICODE_CHAR_FORMAT = r"\x%02x"

print subprocess.mswindows
# getUnicode(os.path.dirname(os.path.realpath(_)), encoding=sys.getfilesystemencoding())
# def getUnicode(value, encoding=None, noneToNull=False):
#     """
#     Return the unicode representation of the supplied value:

#     >>> getUnicode(u'test')
#     u'test'
#     >>> getUnicode('test')
#     u'test'
#     >>> getUnicode(1)
#     u'1'
#     """

#     if noneToNull and value is None:
#         return "NULL"

#     if isinstance(value, unicode):
#         return value
#     elif isinstance(value, basestring):
#         while True:
#             try:
#                 return unicode(value, encoding or "utf8")
#             except UnicodeDecodeError, ex:
#                 try:
#                     return unicode(value, "utf8")
#                 except:
#                     value = value[:ex.start] + "".join(INVALID_UNICODE_CHAR_FORMAT % ord(_) for _ in value[ex.start:ex.end]) + value[ex.end:]
#     elif isListLike(value):
#         value = list(getUnicode(_, encoding, noneToNull) for _ in value)
#         return value
#     else:
#         try:
#             return unicode(value)
#         except UnicodeDecodeError:
#             return unicode(str(value), errors="ignore")  # encoding ignored for non-basestring instances