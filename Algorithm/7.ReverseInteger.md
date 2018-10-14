## Algorithm
* 7.Reverse Integer

	Given a 32-bit signed integer,reverse digits of an integer.
	
	Example:
	
		input:123 output:321
		input:-123 output:-321

	* 解决方案：
		```
		class Solution(object):
		    def reverse(self, x):
		        """
		        :type x: int
		        :rtype: int
		        """
		        if x > pow(2,31) - 1 or x < pow(-2,31):
		            return 0
		        isNegative = x < 0
		        value = str(abs(x))
		        result = value[::-1]
		        result = int(result)
		        if isNegative:
		            result = - result
		        if result > pow(2,31) - 1 or result < pow(-2,31):
		            result = 0
		        return result
		```
	* 字符串反转方法（python）
		* result = value[::-1] ``字符串切片``
		* 列表的reverse方法
			* 方法 1
				* l = list(s)
				* result = "".join(l.reverse())
			* 方法 2
				* l = list(s)
				* result = "".join(l[::-1])
		* reduce
			* result = reduce(lambda x,y:y+x,s)
		* 递归函数
		
			```
			def func(s):
				if len(s) < 1:
				    return s
				return func(s[1:]) + s[0]
			result = func(s)
			```
	   * 使用栈（先进后出）
	  
	   		```
	   		def func(s):
	   			l = list(s)
	   			result = ""
	   			while len(l) > 0:
	   				result += l.pop()
	   			return result
	   		result = func(s)
	   		
	   		```
	   * for循环
	   		* 反向读取
	* other solution  
		