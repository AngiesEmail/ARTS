# -*- coding:utf-8 -*-
import requests

# headers 修改协议头，跳过网站的user-agent的审查
# r.request.headers 输出请求的协议头
# r.request.url 请求的url详细内容

# 搜索关键字提交
# http://www.baidu.com/s?wd=keyword
# http://www.so.com/s?q=keyword

def getHTMLContent(url): 
	try:
		kv = {'user-agent':'Mozilla/5.0'}
		kv1 = {'q':'Python'}
		r = requests.get(url,params=kv1,headers=kv)
		print r.status_code
		print r.request.headers
		print r.request.url
		r.encoding = r.apparent_encoding
		print len(r.text)
		# print r.text[1000:2000]
		r.raise_for_status()	
	except:
		print("爬取失败")


if __name__ == "__main__":
	# url = "https://www.baidu.com/s"
	url = "https://www.so.com/s"
        getHTMLContent(url)



