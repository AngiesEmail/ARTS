## reduce()
* example:
	* reduce(lambda x,y:y+x,s)
* 高阶函数
	* 参数：一个函数f，一个list。
	* 函数f必须接收两个参数，reduce()对list的每个元素反复调用函数f，并返回最终结果值
	* reduce()还可以接收第三个可选参数，作为计算的初始值

## lambda

lambda 只是一个表达式，函数体比def简单很多。

lambda 的主体是一个表达式，而不是一个代码块。仅仅能在lambda表达式中封装有限的逻辑进去。

lambda 表达式是起到一个函数速写的作用。允许在代码内嵌入一个函数的定义。

* lambda x,y : x+y
	* x,y为参数，冒号后为表达式

```
def get_y(a,b):
	return lambda x : ax+b
	
def get_y(a,b):
	def func(x):
		return ax+b
	return func
	
y1 = get_y(1,1)
y1(1)
```
	
	
	
	
	
	
	
	