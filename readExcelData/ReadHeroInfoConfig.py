#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ReadSkillEffectConfig import ReadSkillEffect

class ReadHeroInfo(object):
	"""docstring for ReadHeroInfo"""
	def __init__(self,excelTool):
		super(ReadHeroInfo, self).__init__()
		self._excelTool = excelTool
		self._skillTool = ReadSkillEffect(excelTool)
		self._keyList = ["skill0","skill1(skillId,rate)","skill2(skillId,skillRate)","skill3(skillId,skillRate)","skill4",
						"skill4_2","skill5","skill6","skill7"]

	def readHeroInfo(self,path,key,index):
		config = self._excelTool.getConfigData(path+"HeroInfo.xlsx",key,index)
		if config == None:
			print "HeroInfo中查找不到key值 %s" % key
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
		data["HeroInfo"] = config
		data["SkillEffect"] = skillList
		return data