#!/usr/bin/python
# -*- coding: UTF-8 -*-

class ReadFightingEffectConfig(object):
	"""docstring for ReadFightingEffectConfig"""
	def __init__(self, excelTool,arg):
		super(ReadFightingEffectConfig, self).__init__()
		self.arg = arg
		self._excelTool = excelTool
	
	def readEffectConfig(self,path,key,index):
		config = self._excelTool.getConfigData(path+"FightingEffectConfig.xlsx",key,index)
		if config == None:
			print "FightingEffectConfig中查找不到key值 %s" % key
		return config