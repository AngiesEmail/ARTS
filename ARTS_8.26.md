##A
* 55 Jump Game
	* Description
	
		```
		Given an array of non-negative integers,you are initially positioned 
		at the first index of the array.
		Each element in the array represents your maximum jump length at 		that position.
		Determine if you are able to reach the last index.
		```
	* 思路
		* 只思考了单层的循环，没有思考全面
		* 最终应该用递归的形式去测试，要尝试每一条路径
	* Naming
		* We call a position in the array a "good index" if starting at that position,we can reach the last index. Otherwise,that index is called a "bad index".The problem then reduces to whether or not index 0 is a "good index".
	* Solution
		* This is a dynamic programming question.Usually,solving and fully understanding a dynamic programming problem is a 4 step process:
			
			1. Start with the recursive backtracking solution
			1. Optimize by using a memoization table(top-down dynamic programming)
			2. Remove the need for recursion(bottom-up dynamic programming)
			3. Apply final tricks to reduce the time/memory/ complexity