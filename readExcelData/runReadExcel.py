#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from ReadExcelByOpenpyxl import ReadExcel
from ReadHeroInfoConfig import ReadHeroInfo
from ReadEnemyInfoConfig import ReadEnemyInfo
from ReadLevelInfoConfig import ReadLevelInfo

path = "../../work/DK/Numeric/Development/"

def saveDataToJson(data):
	jsonData = json.dumps(data) 
	f = open("data.json", 'w')
	f.write(jsonData)
	f.close()

if __name__ == "__main__":
	excelTool = ReadExcel()
	heroTool = ReadLevelInfo(excelTool)
	data = heroTool.readLevelData(path,"10101",3)
	saveDataToJson(data)
