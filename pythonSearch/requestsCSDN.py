# -*- coding:utf-8 -*-
# 导入库
import requests
import os
import sys

from bs4 import BeautifulSoup

def getHTMLText(url):
	try: 
		r = requests.get(url)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		demo = r.text
		soup = BeautifulSoup(demo,'html.parser')
		result = soup.article.get_text()
		title = soup.title.get_text()
		path = sys.argv[1]+'/'+title+'.md'
		fileObject = open(path, 'wb') 
		fileObject.write(result.encode('utf-8'))  
		fileObject.close() 
	except:
		return "产生异常"

if __name__=='__main__':
	url = sys.argv[2]
	getHTMLText(url)