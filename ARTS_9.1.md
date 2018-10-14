## Algorithm
* [771.Jewels and Stones](Algorithm/771.JewelsAndStones.md)

	
## Share
* 推导式(python)
	推导式是从一个或者多个迭代器快速简洁地创建数据结构的一种方法。它可以将循环和条件判断结合，从而避免语法冗长的代码。
	
	从一个数据序列构建另一个新的数据序列的结构体
	* 列表推导式
		创建列表的方法，如：[]、list()、str.split().列表推导式也是生成具有一定规律的列表的方法。
		
		列表推导式：使用[]生成list；使用()生成generator（生成器）
		* 示例:
			1. list(range(1,6))
			2. [expression for item in iterable]
			3. [expression for item in iterable if condition]
			4. [expression for item_1 in iterable_1 if condition_1 for item_2 in iterable_2 if condition_2]
	* 字典推导式
		* 示例：
			1. {key_expression : value_expression for expression in iterable}
			2. word = 'letters'  
				letter_count = {letter : word.count(letter) for letter in set(word)}
	* 集合推导式
		* 示例：
			1. {expression for expression in iterable}
	* 生成器推导式
	
		元组是没有推导式的。并不是将列表推导式中的方括号变成圆括号就可以定义元组推导式
		
		nuber_thing = (number for number in range(1,6))
		
		其实，圆括号之间的是生成器推导式，它返回的是一个生成器对象
		
		注：一个生成器只能运行一次。列表、集合、字符串和字典都存储在内存中，但是生成器仅在运行中产生值，不会被存下来。所以不能重新使用或者备份一个生成器。
	* 练习:
	
		```
		>>> names = ['bob','tom','alice','jerry','wendy','smith']
		>>> [name.upper() for name in names if len(name)>3]
		['ALICE', 'JERRY', 'WENDY', 'SMITH']
		>>> [name.lower() for name in names if len(name)>3]
		['alice', 'jerry', 'wendy', 'smith']
		[len(name) for name in names if len(name)>3]
		[5, 5, 5, 5]
		>>> [i for i in range(30) if i % 3 is 0]
		[0, 3, 6, 9, 12, 15, 18, 21, 24, 27]
		>>> def squared(x):
		...     return x*x
		... 
		>>> [squared(i) for i in range(30) if i % 3 is 0]
		[0, 9, 36, 81, 144, 225, 324, 441, 576, 729]
		```
		
## Tips
### unity
* GameObject.Find(name)
	* 此种查询办法：可查找3d场景中的非隐藏的节点
	* 且此方法，查找的节点，是子节点，如果父节点与子节点命名相同，得到的就是子节点。因此，为避免查找错误，则命名时，尽量选择不同。
* EZ Camera的使用
	* 主摄像机（如果是虚拟相机的话，则指的是虚拟相机）必须有一个父节点，而且摄像机的transform的参数均归零。由其父节点的参数来控制。

* 如果将场景A的全部内容复制一份，粘贴到另一个已创建好的场景B中，如果A中的GameObject中挂载了脚本，此时，需要退出unity，重新打开；或者脚本重新挂载。否则实际使用的时候，会找不到

### python
* python中的is与==
	* is 比较的是两个实例对象是不是完全相同，它们是不是同一个对象，占用的内存地址是否相同。
	* == 比较的是两个对象的内容是否相同，即内存地址可以不一样，内容一样就可以了。
	* is运算符比==效率高，在变量和None进行比较时，应该使用is

		
		