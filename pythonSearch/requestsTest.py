# -*- coding:utf-8 -*-
# 导入库
import requests

# 获取一个网址的信息
r = requests.get('http://www.baidu.com')
# 输出一个返回码
print "输出返回码:"
print r.status_code

print "输出编码格式:encoding"
print r.encoding
#  设置获取到的内容的格式
r.encoding = 'utf-8'

# 打印输出的内容 -- 网页信息
print "输出网页内容"
print(r.text)

# requests.request() 构造一个请求，支撑以下各方法的基础方法
# requests.get() 获取HTML网页的主要方法，对应于HTTP的GET
# requests.head() 获取HTML网页头信息的方法，对应于HTTP的HEAD
# requests.post() 向HTML网页提交POST请求的方法，对应于HTTP的HEAD
# requests.put() 向HTML网页提交put请求的方法，对应于HTTP的PUT
# requests.patch() 向HTML网页提交局部修改请求，对应于HTTP的PATCH
# requests.delete() 向HTML页面提交删除请求，对应于HTTP的DELETE
# patch 节省网络带宽

# r = requests.get(url) 构造一个向服务器请求资源的Requests对象,返回一个包含服务器资源的Response的对象
# requests.get(url,params=None,**kwargs)
# **kwargs 
# data/json/headers/cookies/auth/files/timeout/proxies/allow_redirects/stream/verify/cert/
# headers 定制访问协议头
# auth 认证
# proxies 设置代理  隐藏具体的地址 防止逆追踪
# allow_redirects/stream/verify 开关字段
# Response 包含爬虫返回的内容
print "\n 输出r 的类型:"
print type(r)
# 'requests.models.Response'>

print "\n 输出头信息"
print r.headers

print "\n 输出二进制内容"
print r.content

# error 无法赋值备选编码 比encoding 更加精确
# r.apparent_encoding = 'utf-8'

# 异常处理
# requests.ConnectionError 网络连接异常，如DNS查询失败，拒绝连接等
# requests.HTTPError HTTP错误异常
# requests.URLRequired URL 缺失异常
# requests.TooManyRedirects 超过最大重定向次数，产生重定向异常
# requests.ConnectTimeout 连接远程服务器超时异常
# requests.Timeout 请求URL 超时，产生超时异常


# r.raise_for_status() 判断异常，如果不是200，产生异常requests.HTTPError

def getHTMLText(url):
	try: 
		r = requests.get(url)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return "产生异常"



# 分割线
print "========================================"

# HTTP协议
# Hypertext Transfer Protocol 超文本传输协议
# 基于请求与响应，无状态（前后无关联）应用层协议
# 使用url 作为网络资源的标识
# URL:http://host[:port][path]
# path 主机下的具体路径
# 存取资源的internet路径






if __name__=='__main__':
	url = "http://www.baidu.com"
	url1 = "www.baidu.com"
	# print(getHTMLText(url1))


		



