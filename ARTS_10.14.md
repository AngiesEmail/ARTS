## Algorithm
* 14.Longest Common Prefix
	
	Write a function to find the longest common prefix string amongst an array of strings.
	
	if there is no common prefix,return an empty string "".
	
	* 代码
	
		```
		class Solution(object):
		    def longestCommonPrefix(self, strs):
		        """
		        :type strs: List[str]
		        :rtype: str
		        """
		        if len(strs) == 0:
		            return ""
		        firStr = strs[0]
		        result = ""
		        for index in range(len(firStr)):
		            data = firStr[0:index+1]
		            hasSame = True
		            for x in strs:
		                if len(x) == 0 or x[0:index+1] != data:
		                    hasSame = False
		            if hasSame :
		                result = data
		                
		        return result
		```
		
		* 数组、字符临界值考虑
		* python 字符截取 x[m,n] 截取：m到n-1
	* other solution:
	
		```
		class Solution(object):
		    def longestCommonPrefix(self, strs):
		        """
		        :type strs: List[str]
		        :rtype: str
		        """
		        if len(strs) == 0:
		            return ""
		        result = strs[0]
		        for index in range(len(strs)):
		            while strs[index].find(result) != 0:
		                result = result[0:len(result)-1]
		                if result == "":
		                    return result
		                    
		        return result
		```