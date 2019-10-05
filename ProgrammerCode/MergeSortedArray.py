#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
def merge(nums1, m, nums2, n):
    """
    :type nums1: List[int]
    :type m: int
    :type nums2: List[int]
    :type n: int
    :rtype: None Do not return anything, modify nums1 in-place instead.
    """
    if nums1 == None:
        nums1 = nums2
    if nums2 == None:
        return None
    dumpList(nums1)
    dumpList(nums2)
    for x in xrange(0,n):
        nums1[m+x] = nums2[x]
        
    dumpList(nums1)
    # 以上循环等价于
    # nums1.extend(nums2)
    while True :
        if nums1[len(nums1)-1] == 0:
            nums1.pop()
        else:
            break
    dumpList(nums1)
    wholeNum = len(nums1)

    
    for x in xrange(wholeNum-1,-1,-1):
        if x == 0:
            break
        value1 = nums1[x]
        value2 = nums1[x-1]
        if value1 < value2:
            nums1[x] = value2
            nums1[x-1] = value1

    dumpList(nums1)

def dumpList(data):
    value = "["
    for x in xrange(0,len(data)):
        temp = (x == len(data)-1) and "" or ","
        value = value + str(data[x]) + temp
    value = value + "]"
    print(value)

data1 = [4,5,6,0,0,0]
data2 = [1,2,3]
merge(data1,3,data2,3)