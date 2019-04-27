#!/usr/bin/python
# -*- coding: UTF-8 -*-

class ReadSkillEffectConfig(object):
	"""docstring for ReadSkillEffectConfig"""
	def __init__(self,excelTool, arg):
		super(ReadSkillEffectConfig, self).__init__()
		self.arg = arg
		self._excelTool = excelTool
		self._effectConfig = ReadFightingEffectConfig(excelTool)
	
	def readSkillConfig(self,path,key,index):
		if ";" in key:
			key = key.split(";")[0]
		if "," in key:
			key = key.split(",")[0]
		config = self._excelTool.getConfigData(path+"SkillEffect.xlsx",key,index)
		if config == None:
			print "SkillEffect中查找不到key值 %s" % key
			return
		effectInfo = {}
		allValues = config.items()
		for key,value in allValues:
			tag = value["tag"]
			effectData = value.has_key("effects") and value["effects"]
			effectList = None
			if ";" in effectData:
				effectList = effectData.split(";")
			elif "," in effectData:
				effectList = effectData.split(",")
			else:
				effectList.append(effectData)
			if effectList != None:
				for value in effectList:
					effectConfig = self._effectConfig.readEffectConfig(path,value,index)
					effectInfo[tag] = effectConfig

		data = {}
		data["SkillEffect"] = config
		data["FightingEffectConfig"] = effectInfo
		return data



		
		return config