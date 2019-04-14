# -*- coding:utf-8 -*-
import requests

# headers 修改协议头，跳过网站的user-agent的审查
# r.request.headers 输出请求的协议头

def getHTMLContent(url): 
	try:
		kv = {'user-agent':'Mozilla/5.0'}
		r = requests.get(url,headers=kv)
		print r.status_code
		print r.request.headers
		r.encoding = r.apparent_encoding
	        print r.headers
		print r.text[1000:2000]
		r.raise_for_status()	
	except:
		print("爬取失败")


if __name__ == "__main__":
	url = "https://www.amazon.cn/gp/product/B00XBSNK82"
        getHTMLContent(url)



