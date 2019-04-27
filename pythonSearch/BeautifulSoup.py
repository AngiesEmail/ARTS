# -*- coding:utf-8 -*-
# Beautiful soup 库
# pip 安装
# sudo pip install beautifulsoup4
# Beautiful Soup库是解析、遍历、维护‘标签树’的功能库
import requests

r = requests.get('http://python123.io/ws/demo.html')
print r.text
demo = r.text

from bs4 import BeautifulSoup

# html.parser 解释器
soup = BeautifulSoup(demo,'html.parser')
# 输出标题
print soup.title
# 格式化输出内容
print soup.prettify()
