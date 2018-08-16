# ARTS
## Algorithm
1. Implement function ToLowerCase() that has a string parameter str,and returns the same string in lowercase.
	* 考察基础的语法
	* lower 小写
	* upper 大写
	* 32s
	```
	class Solution(object):
	    def toLowerCase(self, str):
	        """
	        :type str: str
	        :rtype: str
	        """
	        return str.lower()
	```
	* 还有就是大写字符与小写字符之间的转换(ASCII码熟悉度)
		* 0-9 对应的ASCII码：48-57
		* 小写字符比大写字符多32（ASCII）
		* A 的ASCII码是：65
		* a 的ASCII码是：97
		* ord(str) 获取str的ASCII码
		* chr(a) 获取ASCII码 a 对应的字符
		* 20s 数组运算比字符运算快
			* "".join(result) list转str
	
		```
		class Solution(object):
		    def toLowerCase(self, str):
		        """
		        :type str: str
		        :rtype: str
		        """
		        result = []
		        for x in str:
		            if x.isalpha() and not x.islower():
		                result.append(chr(ord(x)+32))
		            else:
		                result.append(x)
		        return "".join(result)
		```
	
		* 24s
			* x.isalpha() 至少或都是字符
			* x.islower 是否小写
	
		```
		class Solution(object):
		    def toLowerCase(self, str):
		        """
		        :type str: str
		        :rtype: str
		        """
		        result = ""
		        for x in str:
		            if x.isalpha() and not x.islower():
		                result = result + (chr(ord(x)+32))
		            else:
		                result = result + x
	        	return result
		```
	* 大写变小写 + 32 
		* 20s
		* 右移 5个
		* 2的5次幂是32
		
		```
		class Solution(object):
		    def toLowerCase(self, str):
		        """
		        :type str: str
		        :rtype: str
		        """
		        outputs = []
		        for i in str:
		            outputs.append(chr(ord(i) | (1 <<5)))
		        return "".join(outputs)
		```