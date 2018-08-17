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
		
## Tip

## Share

对于位运算，不是很熟练，所以学下下，顺便分享
* Python 位运算符
	* & 按位与运算符：参与运算的两个值，如果两个相应位都为1，则该位的结果为1，否则为0
	* | 按位或运算符：只要对应的两个二进制位有一个为1时，结果位就为1.
	* ^ 按位异或运算符：当两对应的二进位相异时，结果位1.
	* ~ 按位取反运算符：对数据的每个二进制位取反，即把1变为0，把0变为1.
		* ~x 类似于 -x-1
	* << 左移动运算符：运算符的各二进位全部左移若干位，由``<<``右边的数字指定了移动的位数，高位丢弃，低位补0.
		* 左移 位数  x << n 结果相当于 x乘以2的n次幂
		
		```
		0 0 1 1 1 1 0 0
		1 1 1 1 0 0 0 0
		左移1位，相当于每个二进制乘了2
		左移2位，就相当于每个二进制乘了4（2的2次幂）
		```
	* >> 右移动运算符：把``>>``左边的运算数的各二进位全部右移若干位，``>>``右边的数字指定了移动的位数。
		* 右移 位数 x >> n  结果相当于 x 除以2的n次幂 结果取整