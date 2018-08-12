# ARTS
## Algorithm
* 682. Baseball Game

	 You're now a baseball game point recorder.
	 
	 Given a list of strings,each string can be one of the 4 following types:
	 
	 1.`Integer`(one round's score):Directly represents the number of points you get in this round.
	 
	 2.``+``(one round's score):Represents that the points you get in this round are the sum of the last two ``valid`` round's points.
	 
	 3.``D``(one round's score):Represents that the points you get in this round are the doubled data of last ``valid`` round's points.
	 
	 4.``C``(an operation,which isn't a round's score):Represents the last ``valid`` round's points you get were invalid and should be removed.
	 
	 Each round's operation is permanent and could have an impact on the round before and the round after.
	 
	 You need to return the sum of the points you could get in all the rounds.
	 
	 Note: 
	 	* The size of the input list will be between 1 and 1000.
	 	* Every integer represented in the list will be between -30000 and 30000.
	 	
	* 算法实现（Python）

	```
	class Solution(object):
	    def calPoints(self, ops):
	        """
	        :type ops: List[str]
	        :rtype: int
	        """
	        
	        if len(ops) == 0 or len(ops) > 1000:
	            print "input is invalid"
	            return
	        
	        scoreList = []
	        result = 0
	        lastNum1 = 0
	        lastNum2 = 0
	        
	        def DLastScore(data):
	            if len(data) > 0:
	                num = data[len(data)-1] * 2
	                data.append(num)
	                return num
	            return 0
	        
	        def CLastScore(data):
	            if len(data) > 0:
	                num = data[len(data)-1]
	                del data[len(data)-1]
	                return num
	            return 0
	        
	        def AddTwoScore(data):
	            finalNum = 0
	            if len(data) > 1:
	                num1 = data[len(data)-1]
	                num2 = data[len(data)-2]
	                finalNum = num1 + num2
	            elif len(data) == 1:
	                num = data[len(data)-1]
	                finalNum = num
	            data.append(finalNum)
	            return finalNum
	        
	        for score in ops:
	            if score == "D" :
	                lastNum1 = DLastScore(scoreList)
	                result = result + lastNum1
	            elif score == "C" :
	                lastNum1 = CLastScore(scoreList)
	                result = result - lastNum1
	            elif score == "+" :
	                num = AddTwoScore(scoreList)
	                result = result + num
	            else:
	                num = int(score)
	                if num >= -30000 and num <= 30000:
	                    result = result + num
	                    scoreList.append(num)
	                    
	        return result
	```
	 * 思路
	 	* 一个最终的结果返回值
	 	* 一个包含所有分数的list
	 	* 其中还有输入条件判断以及分数范围判断
	 	* 没考虑到的点
	 		* 读题时，关于``D``和``+``没能完全接受正确信息，只做了最终分数的增加，并没有将其添加到分数列表中
	 * 经验教训:还是要多读几遍题，能完整接受其所表达的信息要求。
	 * 在solution中还看到另外一种解题思路，代码如下：
	 
	 	```
	 	class Solution(object):
		    def calPoints(self, ops):
		        stack = []
		        for op in ops:
		            if op == '+':
		                stack.append(stack[-1] + stack[-2])
		            elif op == 'C':
		                stack.pop()
		            elif op == 'D':
		                stack.append(2 * stack[-1])
		            else:
		                stack.append(int(op))
		
		        return sum(stack)
	 	```
	 	* 其运行时间为28s，比我的解题思路快20s
	 	* 原因分析，对python的列表用法还不够熟悉，需要加强学习以及训练
	 	* 疑问部分：
	 		* 没有条件判断，也没有任何的范围检测，这样不会有问题吗？
	 	* 根据此解决方案，优化代码，如下（运行时间36s）
	 		
	 		```
	 		class Solution(object):
    			def calPoints(self, ops):
			        """
			        :type ops: List[str]
			        :rtype: int
			        """
		        
			        if len(ops) == 0 or len(ops) > 1000:
			            print "input is invalid"
			            return
			        
			        scoreList = []
			        
			        def DLastScore(data):
			            if len(data) > 0:
			                num = data[len(data)-1] * 2
			                data.append(num)
			        
			        def CLastScore(data):
			            if len(data) > 0:
			                num = data[len(data)-1]
			                del data[len(data)-1]
			        
			        def AddTwoScore(data):
			            finalNum = 0
			            if len(data) > 1:
			                num1 = data[len(data)-1]
			                num2 = data[len(data)-2]
			                finalNum = num1 + num2
			            elif len(data) == 1:
			                num = data[len(data)-1]
			                finalNum = num
			            data.append(finalNum)
			        
			        for score in ops:
			            if score == "D" :
			                DLastScore(scoreList)
			            elif score == "C" :
			                CLastScore(scoreList)
			            elif score == "+" :
			                AddTwoScore(scoreList)
			            else:
			                num = int(score)
			                if num >= -30000 and num <= 30000:
			                    scoreList.append(num)
			                    
			        return sum(scoreList)
        ```
