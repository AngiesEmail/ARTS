## Algorithm
**804. Unique Morse Code Words** （摩尔斯编码）

International Morse Code defines a standard encoding where each letter is mapped to a series of dots and dashes,as follows:``"a"`` maps to ``".-"``,``"b"`` maps to ``"-..."``,``"c"`` maps to ``"-.-."``,and so on.

For convenience,the full table for the 26 letters of the English alphabet is given below:

```
[".-","-...","-.-.","-..",".","..-.","--.","....","..",".---","-.-",".-..","--","-.","---",".--.","--.-",".-.","...","-","..-","...-",".--","-..-","-.--","--.."]
```

Now,given a list of words,each word can be written as a concatentation of the Morse code of each letter.For example,"cab" can be written as "-.-.-....-",(which is the concatenation "-.-."+"-..."+".-"). We'll call such a concatenation,the transformation of a word.

Return the number of different transformations among all words we have.

* 解决方案：

	```
	class Solution(object):
	    def uniqueMorseRepresentations(self, words):
	        """
	        :type words: List[str]
	        :rtype: int
	        """
	        dic = {"a":".-","b":"-...","c":"-.-.","d":"-..","e":".","f":"..-.","g":"--.","h":"....","i":"..",
	               "j":".---","k":"-.-","l":".-..","m":"--","n":"-.","o":"---","p":".--.",
	              "q":"--.-","r":".-.","s":"...","t":"-","u":"..-","v":"...-","w":".--","x":"-..-","y":"-.--","z":"--.."}
	        result = []
	        for x in words:
	            result.append("".join([dic[y] for y in x]))
	
	        final = {x : result.count(x) for x in result }
	        
	        return len(final)
	```
	
	```
	class Solution(object):
	    def uniqueMorseRepresentations(self, words):
	        MORSE = [".-","-...","-.-.","-..",".","..-.","--.",
	                 "....","..",".---","-.-",".-..","--","-.",
	                 "---",".--.","--.-",".-.","...","-","..-",
	                 "...-",".--","-..-","-.--","--.."]
	
	        seen = {"".join(MORSE[ord(c) - ord('a')] for c in word)
	                for word in words}
	
	        return len(seen)
	```
	
	* ord() 返回对应字符的 ASCII 数值 
* 总结：
	熟悉使用推导式
	
	
	