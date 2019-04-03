#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
conn = sqlite3.connect('python.db')
c = conn.cursor()
c.execute("select * from python")

conn.close()