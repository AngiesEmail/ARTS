def plusOne(digits):
	length = len(digits)
	for index in xrange(length-1,-1,-1):
		if digits[index] < 9:
			digits[index] = digits[index] + 1
			return digits
		digits[index] = 0

	result = []
	result.append(1)
	for x in xrange(0,length):
		result.append(digits[x-1])
	return result


data = [8,2,3,4,5,9]
# [8,2,3,4,5,4]

print plusOne(data)


