#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string
import os

def test(s):
	print "==="
	print len(s)
	print s.count(' ')
	print s.endswith(' ')
	print s.rfind(' ')
	index = s.rfind(' ')
	print s[index+1:len(s)]


data = "a "
# test(data)

def lengthOfLastWord(s):
	s = s.strip(' ')
	print s + "11"
	if s == "":
		return 0
	if s.endswith(' '):
		return 0
	index = s.rfind(' ')
	print index
	return len(s[index+1:len(s)])


print lengthOfLastWord(data)