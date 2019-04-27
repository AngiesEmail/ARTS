#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json

path = "Development/"

def saveDataToJson(data):
	jsonData = json.dumps(data) 
	f = open("data.json", 'w')
	f.write(jsonData)
	f.close()

if __name__ == "__main__":
	excelTool = ReadExcelByOpenpyxl()
	heroTool = ReadHeroInfoConfig(excelTool)
	data = heroTool.readHeroInfo(path,"Hero101",3)
	saveDataToJson(data)
