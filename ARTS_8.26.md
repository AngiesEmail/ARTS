##Algorithm
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
				* 递归回溯
			1. Optimize by using a memoization table(top-down dynamic programming)
				* 自顶向下动态规划 使用一个记忆table，优化
			2. Remove the need for recursion(bottom-up dynamic programming)
				* 自下向上 动态规划 去除递归
			3. Apply final tricks to reduce the time/memory/ complexity
				* 使用技巧来减少时间空间复杂度
	* Approach 1:Backtracking
	
		This is the inefficient solution where we try every single jump pattern that takes us from the first position to the last.We Start from the first position and jump to every index that is reachable.We repeat the process until last index is reached.When stuck,backtrack.
		
		```
		def canJumpFromPosition(position,nums):
			if position == len(nums) - 1:
				return True
			furthestJump = min(position+nums[position],len(nums) - 1)
			for nextposition in xrange(position+1,furthestJump+1):
				if canJumpFromPosition(nextposition,nums):
					return True
		
			return False
		
		def canJump(nums):
			return canJumpFromPosition(0,nums)
		```
		
		One quick optimization we can do for the code above is to check the ``nextPosition`` from fight to left.
		``for nextposition in xrange(furthestJump,position,-1):``
	* Approach 2:Dynamic Programming Top-down
	
		Top-down Dynamic Programming can be thought of as optimized backtracking.It relies on the observation that once we determine that a certain index is good/bad,this result will never change.This means that we can store the result and not need to recompute it every time.
		
		Therefore,for each position in the array,we remember whether the index is good or bad.Let's call this array ``memo`` and let its values be either one of:GOOD,BAD,UNKONWN.This technique is called memoization.
		* Steps
			1. Initially,all elements of the ``memo`` table are UNKONEW,except for the last one,which is (trivially) GOOD(it cal reach itself)
			2. Modify the backtracking algorithm such that the recursive step first checks if the index is kown(Good/BAD)
				1. If it is known then return True/False
				2. Otherwise perform the backtracking steps as before
			3. Once we determine the value of the current index,we store it in the ``memo`` table.
			
		```
		typeList = ["GOOD","BAD","UNKNOWN"]
		memo = {}
		def canJumpFromPosition(position,nums):
			if memo[position] != typeList[2]:
				return memo[position] == typeList[0] and True or False
			furthestJump = min(position+nums[position],len(nums)-1)
			for nextposition in xrange(position+1,furthestJump+1):
				if canJumpFromPosition(nextposition,nums):
					memo[position] = typeList[0]
					return True
		
			memo[position] = typeList[1]
			return False
		
		def canJump(nums):
			for x in xrange(0,len(nums)):
				memo[x] = typeList[2]
			memo[len(nums)-1] = typeList[0]
			return canJumpFromPosition(0,nums)
		
		data = [2,5,0,0]
		print canJump(data)
		```
	* Approach 3:Dynamic Programming Bottom-up
	
		Top-down to bottom-up conversion is done by eliminating recursion.In practice,this achieves better performances as we no longer have the method stack overhead and might even benefit from some caching.More importantly,this step opens up possibilities for future optimization.The recursion is usually eliminated by trying to reverse the order of the steps from the top-down approach.
		
			conversion 转换
			eliminating 消除 排除
			recursion 递归
			stack overhead 栈开销
		
		The observation to make here is that we only ever jump to the right.This means that if we start from the right of the array,every time we will query a position to our right,that position has already be determined as being GOOD or BAD.This means we don't need to recurse anymore,as we will always hit the ``memo`` table.

			observation 观察 评论
		
		```
		data = [2,5,0,0]
		typeList = ["GOOD","BAD","UNKNOWN"]
		def canJump(nums):
			memo = {}
			for x in xrange(0,len(nums)):
				memo[x] = typeList[2]
		
			memo[len(nums)-1] = typeList[0]
		
			for x in xrange(len(nums)-2,-1,-1):
				furthestJump = min(x+nums[x],len(nums)-1)
				for j in xrange(x+1,furthestJump+1):
					if memo[j] == typeList[0]:
						memo[x] = typeList[0]
						break
			return memo[0] == typeList[0]
		print canJump(data)
		```	
	* Approach 4:Greedy
	
		Once we have our code in the bottom-up state,we can make one final,important observation.From a given position,when we try to see if we can jump to GOOD position,we only ever use one - the first one (see the break statement).In other words,the left-most one.If we keep track of this left-most GOOD position as a separate variable,we can avoid searching for it in the array.Not only that,but we can stop using the array altogether.
		
		```
		def canJump(nums):
			lastPos = len(nums) - 1;
			for i in xrange(len(nums)-1,-1,-1):
				if i + nums[i] >= lastPos:
					lastPos = i
			return lastPos == 0
		```
	* 递归、双层循环、自右向左
	
		```
		递归
		记忆table，减少消耗
		双层循环，消除递归
		自右向左，减少栈消耗
		```