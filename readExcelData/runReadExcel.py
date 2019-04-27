#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from ReadExcelByOpenpyxl import ReadExcel
from ReadHeroInfoConfig import ReadHeroInfo
from ReadEnemyInfoConfig import ReadEnemyInfo

path = "../../work/DK/Numeric/Development/"

def saveDataToJson(data):
	jsonData = json.dumps(data) 
	f = open("data.json", 'w')
	f.write(jsonData)
	f.close()

if __name__ == "__main__":
	excelTool = ReadExcel()
	heroTool = ReadEnemyInfo(excelTool)
	data = heroTool.readEnemyInfo(path,"robot1702",3)
	saveDataToJson(data)
