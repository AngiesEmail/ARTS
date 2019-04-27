#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ReadEnemyInfoConfig import ReadEnemyInfo

class ReadLevelInfo(object):
	"""docstring for ReadLevelInfo"""
	def __init__(self, excelTool):
		super(ReadLevelInfo, self).__init__()
		self._excelTool = excelTool
		self._enemyTool = ReadEnemyInfo(excelTool)


	def readLevelData(self,path,key,index):
		config = self._excelTool.getConfigData(path+"LevelInfo.xlsx",key,index)
		if config == None:
			print "LevelInfo中查找不到key值 %s" % key
			return
		print config
		tag = config.has_key("tag") and config["tag"]
		if tag == None:
			return
		enemyList = {}
		for index in xrange(1,6):
			key = "enemy%d" % index
			enemyId = config.has_key(key) and config[key]
			if enemyId != None:
				enemyInfo = self._enemyTool.readEnemyInfo(path,enemyId,index)
				if enemyInfo != None:
					enemyList[enemyId] = enemyInfo
		
		data = {}
		data["LevelInfo"] = config
		data["EnemyInfo"] = enemyList
		return data
		