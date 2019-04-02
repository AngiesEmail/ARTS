def rewriteSqrt(x):
	print x
	if x == 0:
		return 0
	left = 1
	right = x
	while True:
		mid = left + (right - left) / 2
		if (mid > x/mid):
			right = mid - 1
		else:
			if mid + 1 > x/(mid+1):
				return mid
			left = mid + 1


data = 8
print rewriteSqrt(data)