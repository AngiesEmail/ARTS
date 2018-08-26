# def canJumpFromPosition(position,nums):
# 	if position == len(nums) - 1:
# 		return True
# 	furthestJump = min(position+nums[position],len(nums) - 1)
# 	for nextposition in xrange(position+1,furthestJump):
# 		if canJumpFromPosition(nextposition,nums):
# 			return True

# 	return False

# def canJump(nums):
# 	return canJumpFromPosition(0,nums)

# typeList = ["GOOD","BAD","UNKNOWN"]
# memo = {}
# def canJumpFromPosition(position,nums):
# 	if memo[position] != typeList[2]:
# 		return memo[position] == typeList[0] and True or False
# 	furthestJump = min(position+nums[position],len(nums)-1)
# 	for nextposition in xrange(position+1,furthestJump+1):
# 		if canJumpFromPosition(nextposition,nums):
# 			memo[position] = typeList[0]
# 			return True

# 	memo[position] = typeList[1]
# 	return False

# def canJump(nums):
# 	for x in xrange(0,len(nums)):
# 		memo[x] = typeList[2]
# 	memo[len(nums)-1] = typeList[0]
# 	return canJumpFromPosition(0,nums)

# data = [2,5,0,0]
# print canJump(data)

# typeList = ["GOOD","BAD","UNKNOWN"]
# def canJump(nums):
# 	memo = {}
# 	for x in xrange(0,len(nums)):
# 		memo[x] = typeList[2]

# 	memo[len(nums)-1] = typeList[0]

# 	for x in xrange(len(nums)-2,-1,-1):
# 		furthestJump = min(x+nums[x],len(nums)-1)
# 		for j in xrange(x+1,furthestJump+1):
# 			if memo[j] == typeList[0]:
# 				memo[x] = typeList[0]
# 				break
# 	return memo[0] == typeList[0]

# print canJump(data)

data = [2,5,0,0]
def canJump(nums):
	lastPos = len(nums) - 1;
	for i in xrange(len(nums)-1,-1,-1):
		if i + nums[i] >= lastPos:
			lastPos = i
	return lastPos == 0

print canJump(data)




