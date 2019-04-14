# -*- coding:utf-8 -*-
import requests

# headers 修改协议头，跳过网站的user-agent的审查
# r.request.headers 输出请求的协议头
# r.request.url 请求的url详细内容
# 网络图片的爬取
# http://img0.dili360.com/pic/2019/02/18/5c6a744ce31a94v12817114_t.jpg
# IP地址归属地查询
# www.ip138.com
# http://m.ip138.com/ip.asp?ip=ipaddress


# 搜索关键字提交
# http://www.baidu.com/s?wd=keyword
# http://www.so.com/s?q=keyword

def getHTMLContent(url,ip): 
	try:
		kv = {'ip':ip}
		r = requests.get(url,params=kv)
		print r.status_code
		r.encoding = r.apparent_encoding
		print r.text[-500:]
		r.raise_for_status()	
	except:
		print("爬取失败")


if __name__ == "__main__":
	# url = "https://www.baidu.com/s"
	url = "http://m.ip138.com/ip.asp"
	ip  = '202.204.80.112'
	getHTMLContent(url,ip)



