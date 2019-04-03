#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
conn = sqlite3.connect('python.db')
c = conn.cursor()
c.execute("INSERT INTO python VALUES(6,'如何用Python来发送邮件？','','可以使用smtplib标准库','','邮件;smtplib')")
c.execute("INSERT INTO python VALUES(7,'有没有一个工具可以帮助查找python的bug和进行静态的代码分析？','','有,PyChecker是一个Python代码的静态分析工具，可以帮助查找python代码的bug，会对代码的复杂度和格式提出警告。\n  Pylint是另一个工具可以进行coding standard检查','','PyChecker;静态分析工具;Pylint;coding standard检查')")
conn.commit()
conn.close()











