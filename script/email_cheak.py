#!/usr/bin/env python
# __author__= 'jf'
import re
from lib.core import outputer
output = outputer.outputer()


class spider:

    def run(self,url,html):
        #print(html)
        pattern = re.compile(r'([\w-]+@[\w-]+\.[\w-]+)+')
        email_list = re.findall(pattern, html)
        email_list = list(set(email_list))
        if(email_list):
            for email in email_list:
            	print "[Find email]:" + email
            	output.add_list("email",email)
            return True
        return False