# -*- coding:utf-8 -*-
import requests

# headers 修改协议头，跳过网站的user-agent的审查
# r.request.headers 输出请求的协议头
# r.request.url 请求的url详细内容
# 网络图片的爬取
# http://img0.dili360.com/pic/2019/02/18/5c6a744ce31a94v12817114_t.jpg

# 搜索关键字提交
# http://www.baidu.com/s?wd=keyword
# http://www.so.com/s?q=keyword

def getHTMLContent(url,path): 
	finalPath = path + url.split('/')[-1]
	try:
		r = requests.get(url)
		print r.status_code
		r.encoding = r.apparent_encoding
		with open(finalPath,'wb') as f:
			f.write(r.content)
			f.close()
		r.raise_for_status()	
	except:
		print("爬取失败")


if __name__ == "__main__":
	# url = "https://www.baidu.com/s"
	url = "http://img0.dili360.com/pic/2019/02/18/5c6a744ce31a94v12817114_t.jpg"
	path = '/data/ARTS/pythonSearch/'
	getHTMLContent(url,path)



