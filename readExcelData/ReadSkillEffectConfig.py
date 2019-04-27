#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ReadFightingEffectConfig import ReadFightingEffect

class ReadSkillEffect(object):
	"""docstring for ReadSkillEffect"""
	def __init__(self,excelTool):
		super(ReadSkillEffect, self).__init__()
		self._excelTool = excelTool
		self._effectConfig = ReadFightingEffect(excelTool)
	
	def readSkillConfig(self,path,key,index):
		print "%s   %s  %d" % (type(key),key,key == False)
		if key == False:
			return
		print "="*10
		if ";" in key:
			key = key.split(";")[0]
		if "," in key:
			key = key.split(",")[0]
		config = self._excelTool.getConfigData(path+"SkillEffect.xlsx",key,index)
		if config == None:
			print "SkillEffect中查找不到key值 %s" % key
			return
		effectInfo = []
		tag = config["tag"]
		effectData = config.has_key("effects") and config["effects"]
		if effectData != None:
			effectList = []
			if ";" in effectData:
				effectList = effectData.split(";")
			elif "," in effectData:
				effectList = effectData.split(",")
			else:
				effectList.append(effectData)
			if effectList != None:
				for value in effectList:
					effectConfig = self._effectConfig.readEffectConfig(path,value,index)
					effectInfo.append(effectConfig)
		else:
			print "SkillEffect tag %s has none effects"%(tag)
				

		data = {}
		data["SkillEffect"] = config
		data["FightingEffectConfig"] = effectInfo
		return data



		
		return config