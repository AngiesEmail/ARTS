# -*- coding:utf-8 -*-
# 网络爬虫的问题
# 应用范围
# 1、爬取网页 玩转网页
#     小规模，数据量小，爬取速度不敏感。Requests 库即可
# 2、爬取网站 爬取系列网站
#     中规模 数据规模比较大 爬取速度敏感 Scrapy库
# 3、爬取全网
#     大规模 搜索引擎 爬取速度关键  定制开发
# 网络爬虫会对web服务器产生开销、性能骚扰
# 法律风险
# 隐私泄露
# 可突破简单访问控制的能力
# 网络爬虫的规则
# 限制网络爬虫
#     来源审查：判定User_Agent 协议头信息
#     发布公告： Robots协议
#     
# Robots协议
# Robots Exclusion Standard 网络爬虫排除标准
# 作用：网站告知网络爬虫那些页面可以抓取，那些不行
# 形式：在网站根目录下的robots.txt文件
# 京东:https://www.jd.com/robots.txt
# User-agent:*
# Disallow:
# Robots协议遵守方式
# 网络爬虫：自动或人工识别Robots.txt，再进行内容爬取
# 约束性：Robots协议是建议但非约束性，网络爬虫可以不遵守，但存在法律风险
