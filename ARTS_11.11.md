## Algorithm
* [35. Search Insert Position](Algorithm/35.SearchInsertPosition.md)

## Review


## Tip	
* unity 3d摄像机 场景置灰的效果实现
	* 使用后处理Post Processing
	* 给摄像机增加一个组件：Post Processing Behavior
	* 选中一个默认的配置文件：profile
	* 选中配置文件，在inspector面板中，可看到Color Grading
	* Color Grading的子选项配置Basic中：
		* Post Exposure 更改亮度
		* Saturation 置灰
	* 代码控制
		
		```
		var colorGrading = profile.colorGrading;
		var settings = colorGrading.settings;
		settings.basic.postExposure = -1.2f;
		colorGrading.settings=settings;
		```
		* **重点是第四行，修改完setting之后，将setting再重置回去，否则不会生效**
## Share
* 一个有讲解python源码的博客地址（还有JVM、Tensorflow、数据挖掘）
	[栖迟于一丘](https://www.hongweipeng.com/index.php/series.html)



