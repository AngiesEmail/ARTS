# -*- coding:utf-8 -*-
import requests

def getHTMLContent(url):
	try:
		r = requests.get(url)
		r.raise_for_status()
		print r.status_code
        	r.encoding = r.apparent_encoding
        	print r.text
	except:
		print("爬取失败")


if __name__ == "__main__":
	url = "https://item.jd.com/2967929.html"
        getHTMLContent(url)



