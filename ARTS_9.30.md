## Algorithm
* 9.Palindrome Number （Palindrome 回文--正读，倒读相同）

	Determine whether an integer is a palindrome.An integer is a palindrome when it reads the same backward as forward.
	
	* 思路：将其反转之后，跟原数字比较，是否相同（字符串反转）
	* 解决办法：
	
		```
		class Solution(object):
		    def isPalindrome(self, x):
		        """
		        :type x: int
		        :rtype: bool
		        """
		        data = str(x)[::-1]
		        if data == str(x):
		            return True
		        return False
		```
	* 有关字符反转的部分，参考9.23的文档
	* other solution:
		1. Revert half of the number
			
			The first idea that comes to mind is to convert the number into string, and check if the string is a palindrome,but this would require extra non-constant space(额外的非恒定空间) for creating the string which is not allowed by the problem description.
			
			Second idea would be reverting the number itself,and then compare the number with original number,if they are the same,then the number is a palindrome.However,if the reversed number is larger than int.MAX,we will hit integer overflow problem(遇到整数溢出问题).
			
			Following the thoughts based on the second idea,to avoid the overflow issue of the reverted number,what if we only revert half of the int number? After all,the reverse of the last half of the palindrome should be the same as the first half of the number,if the number is a palindrome.
			
			```
			class Solution(object):
			    def isPalindrome(self, x):
			        """
			        :type x: int
			        :rtype: bool
			        """
			        if x < 0 or (x % 10 == 0 and x != 0):
			            return False
			        revertedNumber = 0
			        while x > revertedNumber:
			            revertedNumber = revertedNumber * 10 + x % 10
			            x /= 10
			        return x == revertedNumber or x == revertedNumber/10
			```
			
			
			
			
			
			
			
			
			