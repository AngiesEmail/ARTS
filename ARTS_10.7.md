## Algorithm
* 13.Roman to integer
	
	Roman numberals are represented by seven different symbols:I,V,X,L,C,D and M.
	```
	Symbol     Value
	I            1
	V            5
	X            10
	L            50
	C            100
	D            500
	M            1000
	```
	
	For example,two is written as II in Roman numberal,just two one's added together.Twelve is written as ,XII,which is simply X + II.The number twenty seven is written as XXVII,which is XX + V + II.
	
	Roman numberals are usually written largest to smallest from left to right.However,the numberal for four is not IIII.Instead,the number four is written as IV.Because the one is before the five we subtract it making four.The same principle applies to the number nine,which is written as IX.There are six instances where subtraction is used:
	
	* I can be placed before V(5) and X(10) to make 4 and 9.
	* X can be placed before L(50) and C(100) to make 40 and 90.
	* C can be placed before D(500) and M(1000) to make 400 and 900.

	Given a roman numberal,convert it to an Integer.Input is guaranteed to be within the range from 1 to 3999.
	
	* 代码：
	
		```
		class Solution(object):
		    def romanToInt(self, s):
		        """
		        :type s: str
		        :rtype: int
		        """
		        data = {"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000}
		        substr = ["IV","IX","XL","XC","CD","CM"]
		        reverseS = s[::-1]
		        index = 0
		        result = 0
		        while index < len(s):
		            if index < len(s) - 1:
		                curStr = s[index]
		                nextStr = s[index + 1]
		                if substr.count(curStr+nextStr) == 1:
		                    result = result - data[curStr] + data[nextStr]
		                    index += 2
		                else:
		                    result = result + data[curStr]
		                    index += 1
		            else:
		                result = result + data.get(s[index])
		                index += 1
		                
		        return result
		```