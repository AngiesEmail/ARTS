## Algorithm
**832. Flipping an Image**

Given a binary matrix ``A``,we want to flip the image horizontally,then invert it,and return the resulting image.

To flip an image horizontally means that each row of the image is reversed.For example,flipping ``[1,1,0]`` horizontally resluts in ``[0,1,1]``.

To invert an image means that each ``0`` is replaced by ``1``,and each ``1`` is replaced by ``0``.For example,inverting ``[0,1,1]`` resluts in ``[1,0,0]``

* 解决方案：

	```
	class Solution(object):
	    def flipAndInvertImage(self, A):
	        """
	        :type A: List[List[int]]
	        :rtype: List[List[int]]
	        """
	        result = []
	        for data in A:
	            data.reverse()
	            result.append([ -x+1 for x in data])
	        return result
	```
	
	* 误区：
		* list.reverse() 翻转没有返回值，会反转原有列表
		* 1与0的替换，一开始用~(按位取反)做，是不正确的
* 其他的解决方案：
	* row[~i] = row[-i-1] = row[len(row) - 1 - i]