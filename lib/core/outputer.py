#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
报告页面生成py
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class outputer:
    data = {}

    # 获取某个数据
    def get(self,key):
        if key in self.data:
            return self.data[key]
        return None

    # 通过字典方式添加数据
    def add(self,key,data):
    	#使用键值对保存data
        self.data[key] = data

    # 通过列表方式添加数据
    def add_list(self,key,data):
    	#创建列表
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(data)

    # 显示加入的数据
    def show(self):
        for key in self.data:
            print "%s:%s"%(key,self.data[key])
    
    #将键值对生成html
    def _build_table(self):
        _str = ""
        for key in self.data:
        	#判断字典中的键是否为列表
            if isinstance(self.data[key],list):
                _td = ""
                for key2 in self.data[key]:
                    _td += key2 + '</br>'
                _str += "<tr><td>%s</td><td>%s</td></tr>"%(key,_td)
            else:
                _str += "<tr><td>%s</td><td>%s</td></tr>"%(key,self.data[key])
        return _str
    #build html
    def build_html(self,filename):
        html_head = '''
        <!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="gbk">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>AjatarScan Report</title>
<link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://cdn.bootcss.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://cdn.bootcss.com/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
<div class="container container-fluid">
	<div class="row-fluid">
		<div class="span12">
			<h3 class="text-center">
				AjatarScan Report
			</h3>
			</BR>
			<table class="table table-bordered">
				<thead>
					<tr>
						<th>
							title
						</th>
						<th>
							content
						</th>
					</tr>
				</thead>
				<tbody>
					build_html_AjatarScan
				</tbody>
			</table>
		</div>
	</div>
</div>  </body>
</html>'''.replace("build_html_AjatarScan",self._build_table())
        file_object = open(filename+'.html', 'w')
        file_object.write(html_head)
        file_object.close()