#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ReadSkillEffectConfig import ReadSkillEffect

class ReadEnemyInfo(object):
	"""docstring for ReadEnemyInfo"""
	def __init__(self,excelTool):
		super(ReadEnemyInfo, self).__init__()
		self._excelTool = excelTool
		self._skillTool = ReadSkillEffect(excelTool)
		self._keyList = ["skill0","skill1(skillId,rate)","skill2","skill3"]

	def readEnemyInfo(self,path,key,index):
		config = self._excelTool.getConfigData(path+"EnemyInfo.xlsx",key,index)
		if config == None:
			print "EnemyInfo中查找不到key值 %s" % key
			return
		tag = config["tag"]
		skillList = {}
		for key in self._keyList:
			skillId = config.has_key(key) and config[key]
			if skillId != None:
				skillInfo = self._skillTool.readSkillConfig(path,skillId,index)
				if skillInfo != None:
					skillList[skillId] = skillInfo
		
		data = {}
		data["EnemyInfo"] = config
		data["SkillEffect"] = skillList
		return data