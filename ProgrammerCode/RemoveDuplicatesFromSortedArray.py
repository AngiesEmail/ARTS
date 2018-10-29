def test(nums):
	if len(nums) == 0:
		return 0
	length = 1
	preValue = nums[0]
	for index in xrange(1,len(nums)):
		if nums[index] > preValue:
			preValue = nums[index]
			nums[length] = preValue
			length = length + 1
	return length

nums = [1,1,2]
print test(nums)