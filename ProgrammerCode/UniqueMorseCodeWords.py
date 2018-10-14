dic = {"a":".-","b":"-...","c":"-.-.","d":"-..","e":".","f":"..-.","g":"--.","h":"....","i":"..",
               "j":".---","k":"-.-","l":".-..","m":"--","n":"-.","o":"---","p":".--.",
              "q":"--.-","r":".-.","s":"...","t":"-","u":"..-","v":"...-","w":".--","x":"-..-","y":"-.--","z":"--.."}
words = ["gin", "zen", "gig", "msg"]  
result = []
for x in words:
	result.append("".join([dic[y] for y in x]))

final = {x : result.count(x) for x in result }
	
print len(final)