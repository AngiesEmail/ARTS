A = [[1,1,0],[1,0,1],[0,0,0]]
result = []
for data in A:
    data.reverse()
    result.append([ -x+1 for x in data])
print result