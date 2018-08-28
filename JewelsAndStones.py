
# def numJewelsInStones(J, S):
#     sDict = {}
#     for s in S:
#         if sDict.get(s, None) == None:
#             sDict[s] = 1
#         else:
#             sDict[s] = sDict.get(s) + 1
#     num = 0
#     for j in J:
#         if sDict.get(j,None) != None:
#             num = num + sDict.get(j)
#     return num

def numJewelsInStones(J, S):
    num = 0
    for x in S:
        if x in J:
            num += 1
    return num

def numJewelsInStones(J,S):
    return sum(s in J for s in S)



J = "aA"
S = "AAABBBB"
print numJewelsInStones(J, S)