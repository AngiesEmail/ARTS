#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
conn = sqlite3.connect('python.db')
c = conn.cursor()
c.execute("INSERT INTO python VALUES(16,'什么是Python？','','Python是一种解释型语言，Python代码在运行之前不需要编译。','','解释型语言')")
conn.commit()
conn.close()











